# 🏆 AI Resume Screening

## 📌 Overview
AI Resume Screening is a **Flask-based** application designed to **automate resume ranking** based on their relevance to a **job description**. The system leverages **Natural Language Processing (NLP)** and **TF-IDF similarity scoring** to evaluate resumes efficiently.

---

## 🚀 Key Features
- 📂 **Multi-format Resume Upload** (PDF/DOCX)
- 📝 **Automated Text Extraction** using PyPDF2 & python-docx
- 🧠 **Advanced NLP Preprocessing** (Tokenization, Lemmatization)
- 📊 **TF-IDF & Cosine Similarity Scoring** for ranking resumes
- 💾 **SQLite Database Integration** for storing rankings
- 🔍 **Retrieve Past Resume Rankings** via API
- ⚡ **REST API with Flask** for seamless interaction
- 🌐 **CORS Enabled** for cross-origin requests
- 🛠 **Robust Logging & Error Handling** for debugging

---

## 🛠️ Tech Stack
| Technology       | Purpose                  |
|-----------------|--------------------------|
| 🐍 **Python**   | Core programming language |
| 🚀 **Flask**    | Backend API framework    |
| 🧠 **Spacy**    | NLP processing engine    |
| 📈 **Scikit-learn** | TF-IDF, Similarity Scoring |
| 📄 **PyPDF2 & python-docx** | Resume parsing |
| 🗄 **SQLite**   | Database storage         |
| 🔗 **Flask-CORS** | Cross-Origin Resource Sharing |

---

## 🔧 Installation Guide
### 📌 Prerequisites
Ensure **Python 3** is installed on your system.

### 📂 Installation Steps
1️⃣ **Clone the Repository**
```bash
git clone https://github.com/yourusername/ai-resume-screening.git
cd ai-resume-screening
```

2️⃣ **Create & Activate a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3️⃣ **Install Required Dependencies**
```bash
pip install -r requirements.txt
```

4️⃣ **Run the Application**
```bash
python app.py
```

5️⃣ Access the application at **`http://127.0.0.1:5000/`** 🚀

---

## 📡 API Endpoints
### 1️⃣ Upload Resume
**🔹 Endpoint:** `POST /upload`
**🔹 Parameters:**
   - `job_description`: Job description text (form-data)
   - `resumes`: List of resume files (PDF/DOCX)
**🔹 Response:** Ranked resumes with similarity scores

### 2️⃣ Retrieve Ranking History
**🔹 Endpoint:** `GET /history`
**🔹 Response:** List of previously ranked resumes with scores & timestamps

---

## 🔮 Future Enhancements
- 📜 **Support for additional file formats** (TXT, ODT, etc.)
- 🤖 **Integration of BERT-based NLP models** for improved ranking
- 💻 **Web-based UI** for a more user-friendly experience
- 🌍 **Integration with job portals** for real-time resume analysis

---

## 📜 License
This project is licensed under the **MIT License**.

