from flask import Flask, render_template, request, send_file, redirect
import os
import sqlite3
from werkzeug.utils import secure_filename

import cloudinary
import cloudinary.uploader

from analytics import generate_analytics
from utils import clean_text, extract_resume_text
from scorer import calculate_scores
from report import generate_pdf

from db.database import init_db
from db.logger import log_usage


# Cloudinary Config
cloudinary.config(
    cloud_name="dwg2nu0ss",
    api_key="134886158831528",
    api_secret="CnKmPh_0KuLhyfLFBbarcnoROoE"
)

app = Flask(__name__)

# Temp storage for Render
UPLOAD_FOLDER = "/tmp/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("db", exist_ok=True)

# Initialize DB
init_db()

latest_results = []


# Home Page
@app.route("/", methods=["GET", "POST"])
def index():
    global latest_results
    results = []

    try:
        if request.method == "POST":

            print("POST request received")

            # Job Description
            job_description = request.form["job_description"]
            job_description = clean_text(job_description)

            # Uploaded Files
            files = request.files.getlist("resumes")

            resume_texts = []
            filenames = []
            uploaded_urls = {}

            # Save, Upload, Extract Text
            for file in files:

                print("Processing:", file.filename)

                if file.filename == "":
                    continue

                filename = secure_filename(file.filename)

                filepath = os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )

                print("Saving temp file:", filepath)

                file.save(filepath)

                # Upload to Cloudinary
                upload_result = cloudinary.uploader.upload(
                    filepath,
                    resource_type="raw"
                )

                file_url = upload_result["secure_url"]

                uploaded_urls[filename] = file_url

                print("Uploaded to Cloudinary:", file_url)

                try:
                    text = extract_resume_text(filepath)
                    text = clean_text(text)
                except Exception as e:
                    print("Resume parsing error:", str(e))
                    text = ""

                resume_texts.append(text)
                filenames.append(filename)

            print("Calculating ATS scores...")

            # Calculate ATS Results
            results = calculate_scores(
                job_description,
                resume_texts,
                filenames
            )

            print("Scores calculated")

            # Store logs in SQLite
            for result in results:
                log_usage(
                    result["resume"],
                    uploaded_urls[result["resume"]],
                    job_description,
                    result["score"]
                )

            latest_results = results

    except Exception as e:
        print("MAIN ERROR:", str(e))
        raise e

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

    conn = sqlite3.connect("db/usage.db")
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

    conn = sqlite3.connect("db/usage.db")
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
        return redirect(file[0])

    return "File not found"


# Main
if __name__ == "__main__":
    app.run(debug=True)