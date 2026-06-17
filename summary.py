import re

def generate_summary(resume_text):
    # Remove emails
    resume_text = re.sub(r'\S+@\S+', '', resume_text)

    # Remove phone numbers
    resume_text = re.sub(r'\+?\d[\d -]{8,}\d', '', resume_text)

    # Remove linkedin/github URLs
    resume_text = re.sub(r'http\S+|www\S+', '', resume_text)

    words = resume_text.split()

    if len(words) > 40:
        summary = " ".join(words[:40]) + "..."
    else:
        summary = " ".join(words)

    return summary