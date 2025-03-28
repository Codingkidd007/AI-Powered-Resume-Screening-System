import os
import re
import PyPDF2
import docx
import pandas as pd
import numpy as np
import joblib
import spacy
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask_cors import CORS
from datetime import datetime
import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load NLP model
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = "uploads"
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Database setup
def init_db():
    conn = sqlite3.connect("resumes.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS resumes (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      filename TEXT,
                      score REAL,
                      uploaded_at TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

# Function to extract text from resumes
def extract_text_from_resume(file_path):
    text = ""
    try:
        if file_path.endswith('.pdf'):
            with open(file_path, "rb") as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                for page in reader.pages:
                    extracted_text = page.extract_text()
                    if extracted_text:
                        text += extracted_text + "\n"
        elif file_path.endswith('.docx'):
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
    except Exception as e:
        logging.error(f"Error extracting text from {file_path}: {e}")
    return text.strip()

# Preprocessing function
def preprocess_text(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
    return " ".join(tokens)

# Function to rank resumes
def rank_resumes(job_description, resumes):
    vectorizer = TfidfVectorizer()
    docs = [preprocess_text(job_description)] + [preprocess_text(resume) for resume in resumes]
    tfidf_matrix = vectorizer.fit_transform(docs)
    similarity_scores = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1:])
    return similarity_scores[0]

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'job_description' not in request.form or 'resumes' not in request.files:
        return jsonify({"error": "Missing job description or resumes"}), 400
    
    job_desc = request.form['job_description']
    files = request.files.getlist("resumes")
    
    resume_texts = []
    valid_files = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            text = extract_text_from_resume(file_path)
            if text:
                resume_texts.append(text)
                valid_files.append(filename)
    
    if not resume_texts:
        return jsonify({"error": "No valid resumes uploaded"}), 400
    
    scores = rank_resumes(job_desc, resume_texts)
    ranked_resumes = sorted(zip(valid_files, scores), key=lambda x: x[1], reverse=True)
    
    # Save ranked resumes to the database
    conn = sqlite3.connect("resumes.db")
    cursor = conn.cursor()
    for file, score in ranked_resumes:
        cursor.execute("INSERT INTO resumes (filename, score, uploaded_at) VALUES (?, ?, ?)",
                       (file, float(score), datetime.now()))
    conn.commit()
    conn.close()
    
    return jsonify({"ranked_resumes": [(file, float(score)) for file, score in ranked_resumes]})

@app.route('/history', methods=['GET'])
def get_history():
    conn = sqlite3.connect("resumes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT filename, score, uploaded_at FROM resumes ORDER BY uploaded_at DESC")
    records = cursor.fetchall()
    conn.close()
    return jsonify({"history": [{"filename": r[0], "score": r[1], "uploaded_at": r[2]} for r in records]})

if __name__ == '__main__':
    app.run(debug=True)
