"""
Diabetes Prediction Model Training Script
=========================================
This script trains a machine learning model for diabetes prediction
using the Diabetes Health Indicators Dataset.

Usage:
    python train_model.py [--data path/to/dataset.csv]

Requirements:
    - Training data with diabetes labels
    - Features as specified in config.json
"""

import argparse
import json
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, classification_report, confusion_matrix
)
import warnings
warnings.filterwarnings('ignore')

# Default configuration
DEFAULT_CONFIG = {
    "model_type": "logistic_regression",
    "threshold": {
        "low": 0.25,
        "medium": 0.5
    },
    "features": [
        'Age', 'BMI', 'PhysHlth', 'Income', 'HighBP', 'HighChol',
        'DiffWalk', 'Stroke', 'HeartDiseaseorAttack', 'GenHlth',
        'Smoker', 'HvyAlcoholConsump', 'PhysActivity', 'VegTables'
    ]
}

FEATURE_COLUMNS = [
    'Age', 'BMI', 'PhysHlth', 'Income', 'HighBP', 'HighChol',
    'DiffWalk', 'Stroke', 'HeartDiseaseorAttack', 'GenHlth',
    'Smoker', 'HvyAlcoholConsump', 'PhysActivity', 'VegTables'
]

TARGET_COLUMN = 'Diabetes_binary'


def load_data(data_path):
    """Load and prepare training data"""
    print(f"Loading data from {data_path}...")

    try:
        df = pd.read_csv(data_path)
        print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None


def preprocess_data(df):
    """Preprocess the data"""
    print("\nPreprocessing data...")

    # Check for required columns
    missing_cols = [col for col in FEATURE_COLUMNS + [TARGET_COLUMN] if col not in df.columns]
    if missing_cols:
        print(f"Warning: Missing columns: {missing_cols}")
        # Try alternative column names
        alt_mapping = {
            'Diabetes_binary': ['Diabetes', 'diabetes', 'Diabetes_012', 'Target'],
            'Age': ['age'],
            'BMI': ['BMI', 'bmi'],
        }
        for missing in missing_cols:
            for col in df.columns:
                if col.lower() in [a.lower() for a in alt_mapping.get(missing, [missing])]:
                    df[missing] = df[col]
                    break

    # Select features and target
    X = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COLUMN].copy()

    # Handle missing values
    X = X.fillna(X.median())

    # Handle outliers (clip extreme values)
    X['BMI'] = X['BMI'].clip(10, 60)
    X['Age'] = X['Age'].clip(18, 100)
    X['PhysHlth'] = X['PhysHlth'].clip(0, 30)

    print(f"Features shape: {X.shape}")
    print(f"Target distribution:\n{y.value_counts(normalize=True)}")

    return X, y


def train_model(X, y, test_size=0.2, random_state=42):
    """Train the diabetes prediction model"""
    print("\n" + "="*50)
    print("Training Model")
    print("="*50)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train Logistic Regression
    print("\nTraining Logistic Regression model...")
    model = LogisticRegression(
        max_iter=1000,
        random_state=random_state,
        class_weight='balanced',
        solver='lbfgs',
        C=1.0
    )

    model.fit(X_train_scaled, y_train)

    # Evaluate on training set
    y_train_pred = model.predict(X_train_scaled)
    y_train_proba = model.predict_proba(X_train_scaled)[:, 1]

    print("\n--- Training Set Performance ---")
    print(f"Accuracy: {accuracy_score(y_train, y_train_pred):.4f}")
    print(f"Precision: {precision_score(y_train, y_train_pred):.4f}")
    print(f"Recall: {recall_score(y_train, y_train_pred):.4f}")
    print(f"F1-Score: {f1_score(y_train, y_train_pred):.4f}")
    print(f"ROC-AUC: {roc_auc_score(y_train, y_train_proba):.4f}")

    # Evaluate on test set
    y_test_pred = model.predict(X_test_scaled)
    y_test_proba = model.predict_proba(X_test_scaled)[:, 1]

    print("\n--- Test Set Performance ---")
    print(f"Accuracy: {accuracy_score(y_test, y_test_pred):.4f}")
    print(f"Precision: {precision_score(y_test, y_test_pred):.4f}")
    print(f"Recall: {recall_score(y_test, y_test_pred):.4f}")
    print(f"F1-Score: {f1_score(y_test, y_test_pred):.4f}")
    print(f"ROC-AUC: {roc_auc_score(y_test, y_test_proba):.4f}")

    print("\n--- Classification Report ---")
    print(classification_report(y_test, y_test_pred))

    print("\n--- Confusion Matrix ---")
    cm = confusion_matrix(y_test, y_test_pred)
    print(cm)

    # Cross-validation
    print("\n--- Cross-Validation (5-fold) ---")
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='roc_auc')
    print(f"CV ROC-AUC: {cv_scores.mean():.4f} (+/- {cv_scores.std()*2:.4f})")

    # Feature importance
    print("\n--- Feature Importance ---")
    feature_importance = pd.DataFrame({
        'feature': FEATURE_COLUMNS,
        'coefficient': model.coef_[0]
    }).sort_values('coefficient', key=abs, ascending=False)
    print(feature_importance.to_string(index=False))

    return model, scaler, X_test_scaled, y_test, y_test_proba


def optimize_threshold(y_test, y_proba):
    """Optimize threshold based on test data"""
    print("\n" + "="*50)
    print("Optimizing Thresholds")
    print("="*50)

    # Find optimal thresholds using different strategies
    thresholds_to_try = np.arange(0.1, 0.9, 0.05)
    best_f1 = 0
    best_threshold = 0.5

    for thresh in thresholds_to_try:
        y_pred = (y_proba >= thresh).astype(int)
        f1 = f1_score(y_test, y_pred)
        if f1 > best_f1:
            best_f1 = f1
            best_threshold = thresh

    print(f"Optimal threshold (for F1): {best_threshold:.2f}")

    # Calculate thresholds for risk levels
    # Low risk: below 25th percentile of positive cases
    # Medium risk: between 25th and 50th percentile
    # High risk: above 50th percentile

    positive_probas = y_proba[y_test == 1]
    low_threshold = np.percentile(positive_probas, 25) * 0.8
    medium_threshold = np.percentile(positive_probas, 50)

    print(f"Recommended thresholds:")
    print(f"  - Low risk: < {low_threshold:.3f}")
    print(f"  - Medium risk: {low_threshold:.3f} - {medium_threshold:.3f}")
    print(f"  - High risk: > {medium_threshold:.3f}")

    return {
        'low': round(low_threshold, 3),
        'medium': round(medium_threshold, 3)
    }


def save_model(model, scaler, config, output_dir='.'):
    """Save the trained model and configuration"""
    import os
    from sklearn.pipeline import Pipeline
    from joblib import dump

    # Create pipeline with scaler
    pipeline = Pipeline([
        ('scaler', scaler),
        ('model', model)
    ])

    # Save model
    model_path = os.path.join(output_dir, 'diabetes_model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(pipeline, f)
    print(f"\nModel saved to: {model_path}")

    # Update and save config
    config['threshold'] = config.get('threshold', {'low': 0.25, 'medium': 0.5})
    config_path = os.path.join(output_dir, 'config.json')
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"Configuration saved to: {config_path}")

    return model_path, config_path


def create_sample_data():
    """Create sample training data if no data file provided"""
    print("\nCreating sample training data...")

    # Generate synthetic diabetes data for demonstration
    np.random.seed(42)
    n_samples = 1000

    data = {
        'Age': np.random.randint(18, 80, n_samples),
        'BMI': np.random.uniform(15, 45, n_samples),
        'PhysHlth': np.random.randint(0, 31, n_samples),
        'Income': np.random.randint(1, 9, n_samples),
        'HighBP': np.random.randint(0, 2, n_samples),
        'HighChol': np.random.randint(0, 2, n_samples),
        'DiffWalk': np.random.randint(0, 2, n_samples),
        'Stroke': np.random.randint(0, 2, n_samples),
        'HeartDiseaseorAttack': np.random.randint(0, 2, n_samples),
        'GenHlth': np.random.randint(0, 2, n_samples),
        'Smoker': np.random.randint(0, 2, n_samples),
        'HvyAlcoholConsump': np.random.randint(0, 2, n_samples),
        'PhysActivity': np.random.randint(0, 2, n_samples),
        'VegTables': np.random.randint(0, 2, n_samples),
    }

    # Create diabetes labels based on risk factors
    diabetes_prob = (
        0.3 * (data['Age'] > 45).astype(int) +
        0.25 * (data['BMI'] > 30).astype(int) +
        0.15 * data['HighBP'] +
        0.1 * data['HighChol'] +
        0.1 * data['GenHlth'] +
        0.1 * (1 - data['PhysActivity'])
    )

    data['Diabetes_binary'] = (np.random.random(n_samples) < diabetes_prob).astype(int)

    df = pd.DataFrame(data)
    return df


def main():
    parser = argparse.ArgumentParser(description='Train Diabetes Prediction Model')
    parser.add_argument('--data', type=str, default=None,
                        help='Path to training data CSV file')
    parser.add_argument('--output', type=str, default='.',
                        help='Output directory for model and config')
    parser.add_argument('--test-size', type=float, default=0.2,
                        help='Test set proportion (default: 0.2)')

    args = parser.parse_args()

    print("="*60)
    print("Diabetes Prediction Model Training")
    print("="*60)

    # Load data
    if args.data:
        df = load_data(args.data)
    else:
        df = create_sample_data()

    if df is None:
        return

    # Preprocess
    X, y = preprocess_data(df)

    # Train model
    model, scaler, X_test, y_test, y_proba = train_model(
        X, y, test_size=args.test_size
    )

    # Optimize thresholds
    threshold = optimize_threshold(y_test, y_proba)

    # Prepare configuration
    config = DEFAULT_CONFIG.copy()
    config['threshold'] = threshold
    config['model_name'] = 'Trained Diabetes Model'
    config['training_date'] = pd.Timestamp.now().strftime('%Y-%m-%d')

    # Save model
    save_model(model, scaler, config, args.output)

    print("\n" + "="*60)
    print("Training Complete!")
    print("="*60)
    print("\nTo start the API server:")
    print("  python app.py")
    print("\nThen open http://localhost:5000 in your browser")


if __name__ == '__main__':
    main()