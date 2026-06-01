# Diabetes Risk Prediction System using Random Forest

## Overview

This project develops a machine learning-based system to predict diabetes risk using the CDC Diabetes Health Indicators dataset.

The model is built using Random Forest Classifier and optimized through hyperparameter tuning, cross-validation, and threshold tuning. The final model is deployed through an interactive Streamlit dashboard to assist users in identifying potential diabetes risk based on health-related indicators.

---

## Dataset

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

## Project Workflow

### 1. Data Preprocessing

- Data Cleaning
- Feature Selection
- Handling Class Imbalance
- Train-Test Split

### 2. Exploratory Data Analysis (EDA)

- Distribution Analysis
- Correlation Analysis
- Diabetes Risk Exploration

### 3. Machine Learning Modeling

Algorithms tested:

- Random Forest
- Logistic Regression
- Decision Tree

### 4. Hyperparameter Tuning

GridSearchCV with 5-Fold Cross Validation

Best Parameters:

```python
{
    'max_depth': 15,
    'min_samples_leaf': 4,
    'min_samples_split': 10,
    'n_estimators': 200
}
