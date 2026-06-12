# Diabetes Prediction System

Website deteksi dini penyakit diabetes berbasis machine learning dengan antarmuka web modern.

## Fitur

- **Input Form**: Formulir input untuk data kesehatan dan gaya hidup
- **Prediksi ML**: Menggunakan model machine learning untuk prediksi risiko diabetes
- **Tampilan Hasil**: Indikator risiko dengan warna (Hijau/Rendah, Kuning/Sedang, Merah/Tinggi)
- **Saran Kesehatan**: Rekomendasi berdasarkan tingkat risiko

## Struktur Proyek

```
diabetes_prediction_system/
├── index.html          # Halaman utama website
├── styles.css          # Desain website
├── script.js           # Logika frontend
├── app.py              # Flask API server
├── train_model.py      # Script training model
├── config.json         # Konfigurasi model dan threshold
├── requirements.txt    # Dependencies Python
├── diabetes_model.pkl  # Model terlatih (auto-generate)
└── README.md           # Dokumentasi
```

## Instalasi

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. (Opsional) Latih Model

Jika Anda memiliki dataset diabetes, latih model sendiri:

```bash
python train_model.py --data path/to/diabetes_data.csv
```

Jika tidak punya dataset, script akan membuat data sample untuk pelatihan demo.

### 3. Jalankan Server

```bash
python app.py
```

Server akan berjalan di `http://localhost:5000`

## Cara Penggunaan

1. Buka browser ke `http://localhost:5000`
2. Isi formulir data kesehatan dan gaya hidup
3. Klik tombol "Prediksi Risiko Diabetes"
4. Lihat hasil prediksi dan saran kesehatan

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Halaman utama |
| `/predict` | POST | Prediksi risiko diabetes |
| `/health` | GET | Health check |
| `/model/info` | GET | Info model |

### Contoh Request Prediction

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Age": 45,
    "BMI": 28.5,
    "PhysHlth": 10,
    "Income": 4,
    "HighBP": 1,
    "HighChol": 0,
    "DiffWalk": 0,
    "Stroke": 0,
    "HeartDiseaseorAttack": 0,
    "GenHlth": 0,
    "Smoker": 0,
    "HvyAlcoholConsump": 0,
    "PhysActivity": 1,
    "VegTables": 1
  }'
```

### Contoh Response

```json
{
  "success": true,
  "probability": 0.35,
  "threshold": {
    "low": 0.25,
    "medium": 0.5
  },
  "risk_level": "Sedang",
  "message": "Risiko diabetes: Sedang"
}
```

## Fitur Input Form

| Field | Tipe | Range | Keterangan |
|-------|------|-------|-------------|
| Age | Number | 18-100 | Usia dalam tahun |
| BMI | Number | 10-60 | Indeks Massa Tubuh |
| PhysHlth | Number | 0-30 | Hari olahraga per bulan |
| Income | Select | 1-8 | Tingkat pendapatan |
| HighBP | Checkbox | 0/1 | Tekanan darah tinggi |
| HighChol | Checkbox | 0/1 | Kolesterol tinggi |
| DiffWalk | Checkbox | 0/1 | Kesulitan berjalan |
| Stroke | Checkbox | 0/1 | Riwayat stroke |
| HeartDiseaseorAttack | Checkbox | 0/1 | Penyakit jantung |
| GenHlth | Checkbox | 0/1 | Kesehatan umum kurang |
| Smoker | Checkbox | 0/1 | Perokok aktif |
| HvyAlcoholConsump | Checkbox | 0/1 | Alkohol berat |
| PhysActivity | Checkbox | 0/1 | Aktif berolahraga |
| VegTables | Checkbox | 0/1 | Makan sayur harian |

## Konfigurasi Threshold

Edit file `config.json` untuk menyesuaikan threshold:

```json
{
  "threshold": {
    "low": 0.25,
    "medium": 0.5
  }
}
```

- **Low** (< 0.25): Risiko Rendah - warna hijau
- **Medium** (0.25 - 0.5): Risiko Sedang - warna kuning
- **High** (> 0.5): Risiko Tinggi - warna merah

## Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Flask (Python)
- **ML**: Scikit-learn (Logistic Regression)
- **Design**: Responsive, Blue/Navy/Orange palette

## Disclaimer

⚠️ **Peringatan**: Website ini hanya untuk alat bantu deteksi dini.
Hasil prediksi TIDAK menggantikan diagnosis dokter.
Konsultasikan selalu dengan profesional kesehatan untuk diagnosis akurat.

## Lisensi

MIT License