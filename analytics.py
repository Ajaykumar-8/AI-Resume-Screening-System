import os
import matplotlib.pyplot as plt
from collections import Counter


def generate_analytics(results):

    os.makedirs("static/charts", exist_ok=True)

    if not results:
        return 0

    plt.style.use("dark_background")

    # -----------------------------
    # Candidate Score Chart
    # -----------------------------
    names = [r["resume"][:10] for r in results]
    scores = [r["score"] for r in results]

    plt.figure(
        figsize=(8, 4),
        facecolor="#1e293b"
    )

    bars = plt.bar(
        names,
        scores,
        color="#60a5fa"
    )

    plt.title(
        "Candidate ATS Scores",
        color="white",
        fontsize=16
    )

    plt.ylabel(
        "Score",
        color="white"
    )

    plt.xticks(
        color="white"
    )

    plt.yticks(
        color="white"
    )

    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.2
    )

    for bar in bars:
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            str(round(bar.get_height(), 1)),
            ha="center",
            color="white"
        )

    plt.tight_layout()

    plt.savefig(
        "static/charts/scores.png",
        facecolor="#1e293b"
    )

    plt.close()

    # -----------------------------
    # Skills Distribution
    # -----------------------------
    all_skills = []

    for r in results:
        all_skills.extend(r["skills"])

    skill_counts = dict(
        Counter(all_skills).most_common(8)
    )

    plt.figure(
        figsize=(8, 4),
        facecolor="#1e293b"
    )

    bars = plt.bar(
        skill_counts.keys(),
        skill_counts.values(),
        color="#93c5fd"
    )

    plt.title(
        "Skills Distribution",
        color="white",
        fontsize=16
    )

    plt.xticks(
        rotation=25,
        color="white"
    )

    plt.yticks(
        color="white"
    )

    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.2
    )

    for bar in bars:
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.05,
            str(int(bar.get_height())),
            ha="center",
            color="white"
        )

    plt.tight_layout()

    plt.savefig(
        "static/charts/skills.png",
        facecolor="#1e293b"
    )

    plt.close()

    # -----------------------------
    # Missing Skills Chart
    # -----------------------------
    all_missing = []

    for r in results:
        all_missing.extend(r["missing_skills"])

    missing_counts = dict(
        Counter(all_missing).most_common(5)
    )

    plt.figure(
        figsize=(8, 4),
        facecolor="#1e293b"
    )

    bars = plt.bar(
        missing_counts.keys(),
        missing_counts.values(),
        color="#bfdbfe"
    )

    plt.title(
        "Skill Gaps Analysis",
        color="white",
        fontsize=16
    )

    plt.xticks(
        rotation=25,
        color="white"
    )

    plt.yticks(
        color="white"
    )

    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.2
    )

    for bar in bars:
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.05,
            str(int(bar.get_height())),
            ha="center",
            color="white"
        )

    plt.tight_layout()

    plt.savefig(
        "static/charts/missing.png",
        facecolor="#1e293b"
    )

    plt.close()

    # -----------------------------
    # Average Score
    # -----------------------------
    avg_score = round(
        sum(scores) / len(scores),
        2
    )

    return avg_score