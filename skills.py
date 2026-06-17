import spacy

nlp = spacy.load("en_core_web_sm")

COMMON_SKILLS = [
    "python",
    "java",
    "sql",
    "machine learning",
    "data analysis",
    "flask",
    "django",
    "power bi",
    "tableau",
    "excel",
    "deep learning",
    "nlp",
    "mongodb",
    "mysql",
    "html",
    "css",
    "javascript",
    "react",
    "node",
    "aws",
    "docker",
    "git"
]


def extract_skills(text):
    text = text.lower()

    found_skills = []

    for skill in COMMON_SKILLS:
        if skill in text:
            found_skills.append(skill)

    return found_skills


def missing_skills(job_desc, resume_text):
    jd_skills = extract_skills(job_desc)
    resume_skills = extract_skills(resume_text)

    missing = list(
        set(jd_skills) - set(resume_skills)
    )

    return missing