import sqlite3
import os


DB_PATH = os.path.join("db", "usage.db")


def log_usage(filename, filepath, job_description, score):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO usage_logs (
            filename,
            filepath,
            job_description,
            score
        )
        VALUES (?, ?, ?, ?)
    """, (
        filename,
        filepath,
        job_description,
        score
    ))

    conn.commit()
    conn.close()