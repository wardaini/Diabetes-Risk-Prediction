# Diabetes Risk Prediction System using Random Forest

## Overview
This project develops a machine learning-based system to predict diabetes risk using the CDC Diabetes Health Indicators dataset. The model is built using Random Forest Classifier and optimized through hyperparameter tuning and cross-validation. The final model is deployed through an interactive web application built with Flask.

---

## Dataset
| Item | Detail |
|---|---|
| Dataset | CDC Diabetes Health Indicators (BRFSS 2014) |
| Source | UCI Machine Learning Repository |
| Total Records | 229,474 (after cleaning) |
| Original Records | 253,680 |
| Class Distribution | 85% No Diabetes / 15% Diabetes |

### Selected Features (10 Features)
| No | Feature | Description |
|---|---|---|
| 1 | HighBP | Riwayat tekanan darah tinggi (0/1) |
| 2 | HighChol | Riwayat kolesterol tinggi (0/1) |
| 3 | CholCheck | Pemeriksaan kolesterol 5 tahun terakhir (0/1) |
| 4 | BMI | Indeks Massa Tubuh |
| 5 | Stroke | Riwayat stroke (0/1) |
| 6 | HeartDiseaseorAttack | Riwayat penyakit jantung (0/1) |
| 7 | PhysActivity | Aktivitas fisik rutin (0/1) |
| 8 | GenHlth | Kondisi kesehatan umum (1-5) |
| 9 | DiffWalk | Kesulitan berjalan (0/1) |
| 10 | Age | Kategori usia (1-13) |

### Target Variable
- `0` = No Diabetes
- `1` = Diabetes

---

## Project Structure
