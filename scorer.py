from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from skills import extract_skills, missing_skills
from summary import generate_summary


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
# RANK LABEL
# -----------------------------
def get_rank_label(score):

    if score >= 90:
        return "Excellent Match"

    elif score >= 70:
        return "Good Match"

    elif score >= 50:
        return "Average Match"

    else:
        return "Poor Match"


# -----------------------------
# CALCULATE SCORES
# -----------------------------
def calculate_scores(
    job_description,
    resume_texts,
    filenames
):

    results = []

    # Combine job description + resumes
    documents = [job_description] + resume_texts

    # TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=5000
    )

    vectors = vectorizer.fit_transform(documents)

    # Cosine similarity
    similarity_scores = cosine_similarity(
        vectors[0:1],
        vectors[1:]
    ).flatten()

    # Process each resume
    for i in range(len(filenames)):

        # TF-IDF score
        tfidf_score = similarity_scores[i] * 100

        # Keyword score
        keyword_score = keyword_match_score(
            job_description,
            resume_texts[i]
        )

        # Important keyword bonus
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

        # Final hybrid score
        final_score = (
            (0.7 * tfidf_score) +
            (0.3 * keyword_score) +
            bonus
        )

        # Max score limit
        if final_score > 100:
            final_score = 100

        # Extract skills
        skills_found = extract_skills(
            resume_texts[i]
        )

        # Find missing skills
        missing = missing_skills(
            job_description,
            resume_texts[i]
        )

        # Rank label
        rank_label = get_rank_label(
            final_score
        )

        # Generate summary
        summary = generate_summary(
            resume_texts[i]
        )

        # Store results
        results.append({
            "resume": filenames[i],
            "score": round(final_score, 2),
            "tfidf_score": round(tfidf_score, 2),
            "keyword_score": round(keyword_score, 2),
            "bonus": bonus,
            "skills": skills_found,
            "missing_skills": missing,
            "rank_label": rank_label,
            "summary": summary
        })

    # Sort by highest score
    results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    return results