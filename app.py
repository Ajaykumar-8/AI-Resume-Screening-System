from flask import Flask, render_template, request

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import pdfplumber
import docx
import os
import re

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# -----------------------------
# CLEAN TEXT
# -----------------------------
def clean_text(text):

    text = text.lower()

    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)

    text = re.sub(r'\s+', ' ', text)

    return text


# -----------------------------
# EXTRACT PDF TEXT
# -----------------------------
def extract_pdf(file_path):

    text = ""

    with pdfplumber.open(file_path) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted + " "

    return text


# -----------------------------
# EXTRACT DOCX TEXT
# -----------------------------
def extract_docx(file_path):

    doc = docx.Document(file_path)

    text = ""

    for para in doc.paragraphs:

        text += para.text + " "

    return text


# -----------------------------
# EXTRACT RESUME TEXT
# -----------------------------
def extract_resume_text(file_path):

    if file_path.endswith('.pdf'):
        return extract_pdf(file_path)

    elif file_path.endswith('.docx'):
        return extract_docx(file_path)

    return ""


# -----------------------------
# KEYWORD MATCH SCORE
# -----------------------------
def keyword_match_score(job_desc, resume):

    job_words = set(job_desc.split())

    resume_words = set(resume.split())

    matched_words = job_words.intersection(resume_words)

    if len(job_words) == 0:
        return 0

    score = (len(matched_words) / len(job_words)) * 100

    return score


# -----------------------------
# HOME PAGE
# -----------------------------
@app.route('/', methods=['GET', 'POST'])
def index():

    results = []

    if request.method == 'POST':

        # Job Description
        job_description = request.form['job_description']

        job_description = clean_text(job_description)

        # Uploaded Files
        files = request.files.getlist('resumes')

        resume_texts = []

        filenames = []

        # Process Resumes
        for file in files:

            if file.filename == '':
                continue

            filepath = os.path.join(
                app.config['UPLOAD_FOLDER'],
                file.filename
            )

            file.save(filepath)

            text = extract_resume_text(filepath)

            text = clean_text(text)

            resume_texts.append(text)

            filenames.append(file.filename)

        # Combine Docs
        documents = [job_description] + resume_texts

        # TF-IDF
        vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1,2),
            max_features=5000
        )

        vectors = vectorizer.fit_transform(documents)

        similarity_scores = cosine_similarity(
            vectors[0:1],
            vectors[1:]
        ).flatten()

        # FINAL HYBRID SCORE
        for i in range(len(filenames)):

            tfidf_score = similarity_scores[i] * 100

            keyword_score = keyword_match_score(
                job_description,
                resume_texts[i]
            )

            # Weighted Hybrid Score
            final_score = (
                (0.7 * tfidf_score) +
                (0.3 * keyword_score)
            )

            # BONUS BOOST
            important_keywords = [
                "python",
                "analytics",
                "data",
                "machine",
                "learning",
                "dashboard",
                "sql",
                "visualization",
                "ai"
            ]

            bonus = 0

            for word in important_keywords:

                if word in resume_texts[i]:
                    bonus += 3

            final_score += bonus

            # Limit Max
            if final_score > 100:
                final_score = 100

            results.append({
                'resume': filenames[i],
                'score': round(final_score, 2)
            })

        # Sort Results
        results = sorted(
            results,
            key=lambda x: x['score'],
            reverse=True
        )

    return render_template(
        'index.html',
        results=results
    )


# -----------------------------
# MAIN
# -----------------------------
if __name__ == '__main__':

    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    app.run(debug=True)