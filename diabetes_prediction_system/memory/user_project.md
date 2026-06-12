---
name: diabetes-prediction-project
description: Website deteksi dini penyakit diabetes dengan ML model
metadata:
  type: project
---

# Proyek: Diabetes Prediction System

**Tujuan:** Membuat website prediksi risiko diabetes berdasarkan data gaya hidup

**Fitur:**
- Input form untuk fitur lifestyle (BMI, HighBP, HighChol, PhysHlth, DiffWalk, Age, dll)
- Prediksi menggunakan model ML (.pkl) dan threshold dari config.json
- Tampilan hasil risiko (Rendah/Sedang/Tinggi) dengan warna indikator
- Flask API backend

**Teknologi:**
- HTML/CSS/JS (Frontend)
- Flask + Python (Backend)
- Scikit-learn model (ML)