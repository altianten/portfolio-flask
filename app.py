# --- 1. TAMBAHKAN IMPORT DI PALING ATAS ---
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)
# --- 2. KONFIGURASI AI ---
# GANTI 'PASTE_API_KEY_DISINI' dengan API Key yang kamu dapat tadi
# Nanti saat deploy ke Render, kita pakai cara yang lebih aman (Environment Variable)
MY_API_KEY = "AIzaSyBGPVpS3DVIg7fxCNmxHRbKO-q7TZuYYxc"
genai.configure(api_key=MY_API_KEY)

# --- 3. CONTEKAN UNTUK AI (DATA DIRIMU) ---
# Ini yang bikin AI-nya pinter soal kamu.
PORTFOLIO_CONTEXT = """
Kamu adalah asisten virtual untuk portfolio Muhammad Septian Nugroho (Ian).
Tugasmu adalah menjawab pertanyaan recruiter atau pengunjung tentang Ian dengan profesional, ramah, dan ringkas.

DATA DIRI:
- Role: Data Scientist, Machine Learning Engineer.
- Skill: Python, SQL, ML (XGBoost), NLP, Streamlit.
- Project: Credit Risk (AUC 0.91), Churn Prediction (97%), Sentiment Analysis.
- Pendidikan: Teknik Informatika UKSW (GPA 3.77).
- Sertifikasi: Oracle SQL, IBM AI.

KONTAK & SOSIAL MEDIA:
- Email: muhammadsian00@gmail.com.
- WhatsApp: +62 82325279005
- LinkedIn: Muhammad Septian Nugroho.
- PENTING: Jika user bertanya kontak, SELALU tambahkan kalimat ini di akhir jawaban: "Atau Bapak/Ibu bisa scroll ke atas di bagian button social media Ian untuk akses cepat."

INSTRUKSI:
- Jawab dalam Bahasa Indonesia yang santai tapi sopan.
- Jika ditanya hal aneh (resep masakan, politik), jawab: "Maaf, saya hanya fokus membahas skill Ian."

GAYA BICARA:
- Gunakan Bahasa Indonesia yang sopan tapi santai (profesional).
- Jika ditanya hal di luar data diri Ian, jawab: "Maaf, saya hanya bisa menjawab seputar profesionalitas Ian."
- Jangan terlalu panjang, langsung ke inti.
"""

# ... (kode projects_data, certs_data, dll biarkan seperti biasa) ...

# ... (sisa kode route home, errorhandler, dll) ...

# --- DATA PROJECTS (Edit di sini, otomatis update di Web) ---
projects_data = [
    {
        "title": "Credit Risk Assessment System",
        # Ganti dengan nama file gambar asli di folder static/img
        "image": "placeholder-credit.png",
        "desc": "Built a robust risk scoring engine achieving an <strong>ROC AUC of ~0.91</strong> to strengthen financial decision-making transparency.",
        "details": [
            "Designed ML pipelines focusing on feature engineering.",
            "Delivered actionable insights through dashboards."
        ],
        "tags": ["Python", "Risk Modeling", "Ensemble"]
    },
    {
        "title": "Churn Prediction",
        "image": "confusion_matrix.png",
        "desc": "Engineered a high-performance churn prediction system achieving <strong>97%+ accuracy</strong> on large-scale datasets.",
        "details": [
            "Solved severe class imbalance using SMOTE.",
            "Optimized stacking ensemble using Optuna."
        ],
        "tags": ["XGBoost", "Optuna", "SMOTE"]
    },
    {
        "title": "E-commerce Sentiment Engine",
        "image": "model_performance.png",
        "desc": "Developed an end-to-end NLP solution analyzing product reviews, achieving <strong>81% precision</strong>.",
        "details": [
            "Benchmarked performance against SVM models.",
            "Deployed the model into a user-facing web application using Streamlit."
        ],
        "tags": ["NLP", "Streamlit", "Deployment"]
    },
    {
        "title": "Hybrid Recommendation Engine",
        "image": "Visualization.png",
        "desc": "Engineered a personalized recommendation system processing <strong>100k+ interactions</strong> using Amazon dataset.",
        "details": [
            "Implemented Hybrid approach: Collaborative Filtering & Content-Based.",
            "Handled data sparsity using dimensionality reduction."
        ],
        "tags": ["SVD", "TF-IDF", "Scikit-learn"]
    },
    {
        "title": "E-Commerce Purchase Prediction",
        "image": "feature_importance.png",
        "desc": "Designed a high-precision ML pipeline achieving <strong>98%+ accuracy, F1, and ROC-AUC</strong> to predict user purchase intent effectively.",
        "details": [
            "Engineered a synthetic dataset of <strong>100k+ records</strong> to simulate complex real-world user behaviors.",
            "Built a robust Stacking Ensemble (XGBoost, LightGBM, CatBoost, Random Forest) optimized with Optuna."
        ],
        "tags": ["Stacking Ensemble", "Optuna", "Predictive Modeling"]
    }
]

# --- DATA CERTIFICATES ---
certs_data = [
    {"title": "Database Design & Programming with SQL", "issuer": "Oracle Academy"},
    {"title": "Database Programming with PL/SQL", "issuer": "Oracle Academy"},
    {"title": "Artificial Intelligence Fundamentals", "issuer": "IBM"}
]
# ... (Data Certs di atas ini biarkan saja)

# --- DATA PELATIHAN (NEW SECTION) ---
profdev_data = [
    {
        "title": "Python Fundamental for Data Science",
        "organizer": "DQLab",
        "year": "2022",
        "desc": "Mastered core Python programming concepts with a specific focus on data manipulation structures and algorithmic logic for analytics.",
        "tags": ["Python", "Data Logic", "Scripting"]
    },
    {
        "title": "DevOps CI/CD Development",
        "organizer": "BuildWithAngga",
        "year": "2022",
        "desc": "Implemented Continuous Integration/Continuous Deployment (CI/CD) pipelines to automate workflows and ensure code integrity in collaborative environments.",
        "tags": ["Github", "CI/CD Automation", "NodeJS", "Version Control"]
    },
    {
        "title": "Full-Stack Website Developer",
        "organizer": "BuildWithAngga",
        "year": "2021",
        "desc": "Gained end-to-end development skills, ranging from UI/UX prototyping to backend architecture. Capable of building user-centric interfaces for data applications.",
        "tags": ["Laravel", "PHP", "Adobe XD", "InVision", "Bootstrap"]
    }
]


@app.route('/')
def home():
    # JANGAN LUPA: Tambahkan 'trainings=trainings_data' di dalam kurung ini
    return render_template('index.html', projects=projects_data, certs=certs_data, profdev=profdev_data)


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message')

        # Panggil Gemini API
        model = genai.GenerativeModel("models/gemini-2.5-pro")
        chat_session = model.start_chat(history=[
            {"role": "user", "parts": [PORTFOLIO_CONTEXT]},
            {"role": "model", "parts": ["Siap, saya mengerti. Silakan tanya."]}
        ])

        response = chat_session.send_message(user_message)
        return jsonify({"reply": response.text})

    except Exception as e:
        print(f"ERROR GEMINI: {e}")  # Cek terminal kalau error lagi
        return jsonify({"reply": "Maaf, otak AI saya sedang gangguan. Coba lagi nanti!"}), 500


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
