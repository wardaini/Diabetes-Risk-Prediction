// Diabetes Prediction System - Frontend JavaScript
// Handles form validation, API calls, and result display

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    const predictBtn = document.getElementById('predictBtn');
    const resultContainer = document.getElementById('resultContainer');
    const loadingOverlay = document.getElementById('loadingOverlay');

    // Check server connectivity on page load
    function checkServerHealth() {
        const API_URL = 'http://localhost:5000/health';

        fetch(API_URL, { method: 'GET', mode: 'cors' })
            .then(response => {
                if (response.ok) {
                    console.log('✓ Server is running and accessible');
                    return response.json();
                } else {
                    console.warn('⚠ Server responded with status:', response.status);
                }
            })
            .then(data => {
                console.log('Server health:', data);
            })
            .catch(error => {
                console.error('✗ Cannot connect to server at http://localhost:5000');
                console.error('Make sure to:');
                console.error('  1. Run the Flask app: python app.py');
                console.error('  2. Access via http://localhost:5000 (not file://)');
                console.error('  3. Check if port 5000 is already in use');
                console.error('Error details:', error.message);
            });
    }

    // Check server on page load
    checkServerHealth();

    // Health tips based on risk level
    const healthTips = {
        low: [
            "Pertahankan pola makan seimbang dengan banyak sayuran dan buah-buahan",
            "Lanjutkan rutinitas olahraga minimal 30 menit per hari",
            "Periksaan kesehatan rutin setiap tahun",
            "Tidur yang cukup 7-8 jam per hari"
        ],
        medium: [
            "Kurangi konsumsi gula dan makanan tinggi lemak",
            "Naikkan intensitas olahraga menjadi 45-60 menit per hari",
            "Kontrol berat badan agar berada di range normal",
            "Kurangi stres dan istirahat yang cukup",
            "Konsultasikan dengan dokter untuk pemeriksaan lebih lanjut"
        ],
        high: [
            "SEGERA konsultasikan dengan dokter untuk pemeriksaan lengkap",
            "Kontrol pola makan secara ketat - hindari gula dan karbohidrat sederhana",
            "Lakukan olahraga rutin tapi sesuai anjuran dokter",
            "Monitor tekanan darah dan kadar gula darah secara berkala",
            "Pertahankan berat badan ideal dengan program yang aman",
            "Ikuti semua anjuran medis dengan serius"
        ]
    };

    // Mapping pertanyaan ke fitur model
    const questionToFeature = {
        // Data Kesehatan Dasar → BMI
        'usia': 'BMI',
        'jenis_kelamin': 'BMI',
        'berat_badan': 'BMI',
        'tinggi_badan': 'BMI',
        'lingkar_pinggang': 'BMI',
        'riwayat_diabetes_keluarga': 'BMI',

        // Kondisi Kesehatan → HighBP dan HighChol
        'riwayat_hipertensi_keluarga': 'HighBP',
        'tekanan_darah_tinggi': 'HighBP',
        'riwayat_kolesterol_keluarga': 'HighChol',
        'kolesterol_tinggi': 'HighChol',
        'cek_kolesterol_5tahun': 'HighChol',
        'obat_hipertensi': 'HighBP',

        // Gaya Hidup → PhysActivity dan GenHlth
        'frekuensi_olahraga': 'PhysActivity',
        'aktivitas_fisik': 'PhysActivity',
        'merokok': 'GenHlth',
        'konsumsi_alkohol': 'GenHlth',
        'konsumsi_sayur': 'GenHlth',
        'makanan_berlemak': 'HighChol'
    };

    // Konversi nilai pertanyaan ke nilai fitur model
    function convertToModelFeatures(formData) {
        const modelData = {
            BMI: 0,
            HighBP: 0,
            HighChol: 0,
            PhysActivity: 0,
            GenHlth: 1,
            CholCheck: 0
        };

        // Hitung BMI dari berat dan tinggi badan
        const berat = parseFloat(formData.berat_badan);
        const tinggi = parseFloat(formData.tinggi_badan);

        if (berat && tinggi && tinggi > 0) {
            const tinggiMeter = tinggi / 100;
            const bmi = berat / (tinggiMeter * tinggiMeter);
            modelData.BMI = Math.round(bmi * 10) / 10;
        }

        // Usia влияет на риск диабета (через BMI)
        if (formData.usia) {
            const usia = parseInt(formData.usia);
            // Если возраст > 45, увеличиваем базовый риск
            if (usia > 45) {
                modelData.BMI += 2; // Повышаем "виртуальный" BMI
            }
        }

        // Riwayat keluarga diabetes → meningkat risiko
        const riwayatDiabetes = formData.riwayat_diabetes_keluarga;
        if (riwayatDiabetes && riwayatDiabetes !== 'tidak') {
            modelData.BMI += 3; // Повышаем риск
        }

        // Kondisi Kesehatan - HighBP
        const riwayatHipertensi = formData.riwayat_hipertensi_keluarga;
        const tekananDarahTinggi = formData.tekanan_darah_tinggi;
        const obatHipertensi = formData.obat_hipertensi;

        if (riwayatHipertensi === 'ada' || tekananDarahTinggi === 'ya' || obatHipertensi === 'ya') {
            modelData.HighBP = 1;
        }

        // Kondisi Kesehatan - HighChol
        const riwayatKolesterol = formData.riwayat_kolesterol_keluarga;
        const kolesterolTinggi = formData.kolesterol_tinggi;
        const cekKolesterol = formData.cek_kolesterol_5tahun;

        if (riwayatKolesterol === 'ada' || kolesterolTinggi === 'ya') {
            modelData.HighChol = 1;
        }

        if (cekKolesterol === 'ya') {
            modelData.CholCheck = 1;
        }

        // Gaya Hidup - PhysActivity
        const frekuensiOlahraga = formData.frekuensi_olahraga;
        const aktivitasFisik = formData.aktivitas_fisik;

        if (frekuensiOlahraga === '2_3_kali' || frekuensiOlahraga === '4_lebih') {
            modelData.PhysActivity = 1;
        }

        if (aktivitasFisik === 'ya') {
            modelData.PhysActivity = 1;
        }

        // Gaya Hidup - GenHlth
        const merokok = formData.merokok;
        const alkohol = formData.konsumsi_alkohol;
        const sayur = formData.konsumsi_sayur;
        const lemak = formData.makanan_berlemak;

        // Merokok снижает здоровье
        if (merokok === 'ya') {
            modelData.GenHlth += 2;
        } else if (merokok === 'former') {
            modelData.GenHlth += 1;
        }

        // Alkohol
        if (alkohol === 'sering') {
            modelData.GenHlth += 2;
        } else if (alkohol === 'sedang') {
            modelData.GenHlth += 1;
        }

        // Konsumsi sayur - baik untuk kesehatan
        if (sayur === 'banyak' || sayur === 'cukup') {
            modelData.GenHlth = Math.max(1, modelData.GenHlth - 1);
        } else if (sayur === 'sangat_sedikit') {
            modelData.GenHlth += 2;
        }

        // Makanan berlemak
        if (lemak === 'sangat_sering' || lemak === 'sering') {
            modelData.HighChol = 1;
            modelData.GenHlth += 1;
        }

        // BMI validation
        if (modelData.BMI < 10 || modelData.BMI > 60) {
            modelData.BMI = 25; // Default value
        }

        // GenHlth should be 1-5
        modelData.GenHlth = Math.min(5, Math.max(1, modelData.GenHlth));

        console.log('Converted model data:', modelData);
        return modelData;
    }

    // Form validation rules
    const validationRules = {
        BMI: { min: 10, max: 60, message: "BMI harus antara 10-60" },
        GenHlth: { min: 1, max: 5, message: "Kesehatan umum harus antara 1-5" }
    };

    // Validate single input
    function validateInput(fieldName, value) {
        const rules = validationRules[fieldName];
        if (!rules) return true;

        const numValue = parseFloat(value);
        if (isNaN(numValue)) return false;
        if (numValue < rules.min || numValue > rules.max) return false;
        return true;
    }

    // Show error state
    function showError(fieldName, message) {
        const field = document.getElementById(fieldName);
        if (!field) return;

        const formGroup = field.closest('.form-group');
        if (!formGroup) return;
        formGroup.classList.add('error');

        let errorMsg = formGroup.querySelector('.error-message');
        if (!errorMsg) {
            errorMsg = document.createElement('span');
            errorMsg.className = 'error-message';
            formGroup.appendChild(errorMsg);
        }
        errorMsg.textContent = message;
    }

    // Clear error state
    function clearError(fieldName) {
        const field = document.getElementById(fieldName);
        if (!field) return;

        const formGroup = field.closest('.form-group');
        if (!formGroup) return;
        formGroup.classList.remove('error');
    }

    // Validate entire form
    function validateForm() {
        let isValid = true;
        const formData = {};

        // Get all form fields
        const form = document.getElementById('predictionForm');
        const formElements = form.elements;

        for (let i = 0; i < formElements.length; i++) {
            const element = formElements[i];

            if (element.name && element.type !== 'submit' && element.type !== 'reset') {
                const value = element.value;

                clearError(element.name);

                if (!value && element.hasAttribute('required')) {
                    showError(element.name, 'Field ini wajib diisi');
                    isValid = false;
                } else if (value) {
                    formData[element.name] = value;
                }
            }
        }

        return { isValid, formData };
    }

    // Get risk level and color class based on probability
    function getRiskLevel(probability, threshold) {
        if (probability < threshold.low) {
            return { level: 'Rendah', class: 'low', color: '#06d6a0' };
        } else if (probability < threshold.medium) {
            return { level: 'Sedang', class: 'medium', color: '#ffd166' };
        } else {
            return { level: 'Tinggi', class: 'high', color: '#ef476f' };
        }
    }

    // Display results
    function displayResults(data) {
        const probability = data.probability;
        // Gunakan display_threshold untuk menentukan kategori risiko (untuk tampilan user)
        // threshold tetap digunakan untuk logika internal model
        const displayThreshold = data.display_threshold || data.threshold;

        // Get risk level berdasarkan display_threshold (untuk tampilan yang lebih masuk akal)
        const risk = getRiskLevel(probability, displayThreshold);

        // Update risk circle
        const riskCircle = document.getElementById('riskCircle');
        riskCircle.className = 'risk-circle ' + risk.class;
        document.getElementById('riskPercentage').textContent = (probability * 100).toFixed(1) + '%';

        // Update risk label
        const riskLabel = document.getElementById('riskLabel');
        riskLabel.textContent = risk.level;
        riskLabel.className = 'risk-label ' + risk.class;

        // Update details
        document.getElementById('riskLevel').textContent = risk.level;
        document.getElementById('probability').textContent = (probability * 100).toFixed(2) + '%';

        // Update health tips
        const tipsList = document.getElementById('tipsList');
        tipsList.innerHTML = '';
        const tips = healthTips[risk.class] || healthTips.low;
        tips.forEach(tip => {
            const li = document.createElement('li');
            li.textContent = tip;
            tipsList.appendChild(li);
        });

        // Show result container
        resultContainer.style.display = 'block';
        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    // Show error message
    function showErrorMessage(message) {
        resultContainer.style.display = 'block';
        const resultContent = resultContainer.querySelector('.result-content');
        resultContent.innerHTML = `
            <div style="color: #ef476f; padding: 20px;">
                <h3>⚠️ Terjadi Kesalahan</h3>
                <p>${message}</p>
            </div>
        `;
    }

    // Make API call
    async function makePrediction(formData) {
        const API_URL = 'http://localhost:5000/predict';

        console.log('Sending prediction request to:', API_URL);
        console.log('Form data:', formData);

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
                mode: 'cors',
                credentials: 'omit'
            });

            console.log('Response status:', response.status);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('Prediction result:', data);
            return data;
        } catch (error) {
            console.error('Prediction error:', error);
            throw error;
        }
    }

    // Handle form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Validate form
        const { isValid, formData } = validateForm();
        if (!isValid) {
            return;
        }

        // Convert form data to model features
        const modelData = convertToModelFeatures(formData);

        console.log('Form data:', formData);
        console.log('Model data:', modelData);

        // Show loading
        loadingOverlay.style.display = 'flex';
        predictBtn.disabled = true;

        try {
            // Make prediction
            const result = await makePrediction(modelData);

            // Display results
            displayResults(result);
        } catch (error) {
            // Show error message
            console.error('Prediction error details:', error.message);

            // Check if it's a network error or connection refused
            if (error.message.includes('Failed to fetch') || error instanceof TypeError) {
                showErrorMessage('Tidak dapat terhubung ke server. Pastikan:\n1. Flask API sedang berjalan di http://localhost:5000\n2. Akses aplikasi melalui http://localhost:5000 (bukan file lokal)\n\nError: ' + error.message);
            } else {
                showErrorMessage('Tidak dapat terhubung ke server. Pastikan Flask API sedang berjalan.\n\nError: ' + error.message);
            }
        } finally {
            // Hide loading
            loadingOverlay.style.display = 'none';
            predictBtn.disabled = false;
        }
    });

    // Handle form reset
    form.addEventListener('reset', function() {
        resultContainer.style.display = 'none';

        // Clear all error states
        document.querySelectorAll('.form-group.error').forEach(group => {
            group.classList.remove('error');
        });
    });

    // Real-time validation on input
    document.querySelectorAll('input[type="number"], select').forEach(field => {
        field.addEventListener('blur', function() {
            if (this.value && validationRules[this.id]) {
                if (validateInput(this.id, this.value)) {
                    clearError(this.id);
                } else {
                    showError(this.id, validationRules[this.id].message);
                }
            }
        });
    });
});

// Fallback prediction function (for testing without API)
function localPredict(formData) {
    // Simulated prediction logic (replace with actual model in production)
    let score = 0;

    // Age factor
    if (formData.Age > 45) score += 0.15;
    if (formData.Age > 55) score += 0.1;

    // BMI factor
    if (formData.BMI > 25) score += 0.15;
    if (formData.BMI > 30) score += 0.15;

    // Health conditions
    if (formData.HighBP) score += 0.15;
    if (formData.HighChol) score += 0.1;
    if (formData.DiffWalk) score += 0.1;
    if (formData.Stroke) score += 0.15;
    if (formData.HeartDiseaseorAttack) score += 0.15;
    if (formData.GenHlth) score += 0.1;

    // Lifestyle factors
    if (formData.Smoker) score += 0.1;
    if (formData.HvyAlcoholConsump) score += 0.1;
    if (!formData.PhysActivity) score += 0.1;
    if (!formData.VegTables) score += 0.05;

    // Physical health
    if (formData.PhysHlth < 10) score += 0.05;

    // Normalize score
    const probability = Math.min(score, 1);

    return {
        probability: probability,
        threshold: {
            low: 0.25,
            medium: 0.5
        }
    };
}