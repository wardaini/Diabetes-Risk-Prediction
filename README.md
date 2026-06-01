# Diabetes Risk Prediction System using Random Forest

# Overview

This project develops a machine learning-based system to predict diabetes risk using the CDC Diabetes Health Indicators dataset.

The model is built using Random Forest Classifier and optimized through hyperparameter tuning, cross-validation, and threshold tuning. The final model is deployed through an interactive Streamlit dashboard to assist users in identifying potential diabetes risk based on health-related indicators.

---

# Dataset

Dataset:
CDC Diabetes Health Indicators

Total Records:
229,474

Selected Features:

1. HighBP
2. HighChol
3. CholCheck
4. BMI
5. PhysActivity
6. GenHlth

Target Variable:

- 0 = No Diabetes
- 1 = Diabetes

---

# Project Workflow

## 1. Data Preprocessing

- Data Cleaning
- Feature Selection
- Handling Class Imbalance
- Train-Test Split

## 2. Exploratory Data Analysis (EDA)

- Distribution Analysis
- Correlation Analysis
- Diabetes Risk Exploration

## 3. Machine Learning Modeling

Algorithms tested:

- Random Forest
- Logistic Regression
- Decision Tree

## 4. Hyperparameter Tuning

GridSearchCV with 5-Fold Cross Validation

Best Parameters:

```python
{
    'max_depth': 15,
    'min_samples_leaf': 4,
    'min_samples_split': 10,
    'n_estimators': 200
}
```

## 5. Model Evaluation

### Metrics

- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC

### Optimized Random Forest Results

| Metric | Score |
|---------|---------|
| Accuracy | 0.7081 |
| Precision | 0.8410 |
| Recall | 0.7081 |
| F1-Score | 0.7469 |
| ROC-AUC | 0.7903 |

---

## 6. Threshold Optimization

Threshold tuning was performed to improve diabetes case detection while maintaining acceptable classification performance.

---

## 7. Deployment

The final model is deployed using Streamlit.

### Users can:

- Enter health indicators
- Predict diabetes risk
- Receive instant prediction results

---

## Feature Importance

### Random Forest Feature Importance Ranking

| Rank | Feature | Importance |
|---------|---------|---------|
| 1 | GenHlth | 0.3101 |
| 2 | HighBP | 0.2992 |
| 3 | BMI | 0.2355 |
| 4 | HighChol | 0.1169 |
| 5 | CholCheck | 0.0223 |
| 6 | PhysActivity | 0.0159 |

General Health (**GenHlth**) was identified as the most influential predictor of diabetes risk.

---

## Technology Stack

- Python
- Pandas
- NumPy
- Scikit-Learn
- Matplotlib
- Joblib
- Streamlit

---

## Installation

### Clone Repository

```bash
git clone https://github.com/username/diabetes-risk-prediction.git
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Streamlit Application

```bash
streamlit run app.py
```

## Key Achievements

- Developed a diabetes risk prediction model using Random Forest.
- Performed feature selection and hyperparameter tuning.
- Achieved ROC-AUC of 0.7903 on the test dataset.
- Conducted 5-Fold Cross Validation to evaluate model stability.
- Built an interactive Streamlit dashboard for real-time prediction.

## Author

**Wardatul A'ani**  
Informatics Engineering Student  
Universitas Malikussaleh  
Indonesia
