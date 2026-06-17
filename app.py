from flask import Flask, render_template, request, send_file
import os
import sqlite3
from werkzeug.utils import secure_filename

from analytics import generate_analytics
from utils import clean_text, extract_resume_text
from scorer import calculate_scores
from report import generate_pdf

from db.database import init_db
from db.logger import log_usage


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

latest_results = []


# Home Page
@app.route("/", methods=["GET", "POST"])
def index():
    global latest_results

    results = []

    if request.method == "POST":

        # Job Description
        job_description = request.form["job_description"]
        job_description = clean_text(job_description)

        # Uploaded Files
        files = request.files.getlist("resumes")

        resume_texts = []
        filenames = []

        # Save and Extract Text
        for file in files:

            if file.filename == "":
                continue

            filename = secure_filename(file.filename)

            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            file.save(filepath)

            text = extract_resume_text(filepath)
            text = clean_text(text)

            resume_texts.append(text)
            filenames.append(filename)

        # Calculate ATS Results
        results = calculate_scores(
            job_description,
            resume_texts,
            filenames
        )

        # Store logs in SQLite
        for result in results:
            log_usage(
                result["resume"],
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    result["resume"]
                ),
                job_description,
                result["score"]
            )

        latest_results = results

    return render_template(
        "index.html",
        results=results
    )


# Download PDF Report
@app.route("/download-report")
def download_report():
    global latest_results

    pdf_path = generate_pdf(latest_results)

    return send_file(
        pdf_path,
        as_attachment=True
    )


# Analytics Dashboard
@app.route("/dashboard")
def dashboard():
    global latest_results

    avg_score = generate_analytics(
        latest_results
    )

    return render_template(
        "dashboard.html",
        avg_score=avg_score
    )


# Admin Panel
@app.route("/admin")
def admin():

    conn = sqlite3.connect(
        "db/usage.db"
    )

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM usage_logs
        ORDER BY created_at DESC
    """)

    logs = cursor.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        logs=logs
    )


# Download User Resume
@app.route("/download-user-resume/<filename>")
def download_user_resume(filename):

    conn = sqlite3.connect(
        "db/usage.db"
    )

    cursor = conn.cursor()

    cursor.execute("""
        SELECT filepath FROM usage_logs
        WHERE filename = ?
        ORDER BY id DESC
        LIMIT 1
    """, (filename,))

    file = cursor.fetchone()

    conn.close()

    if file:
        return send_file(
            file[0],
            as_attachment=True
        )

    return "File not found"


# Main
if __name__ == "__main__":

    init_db()

    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    app.run(debug=True)