from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime


def generate_pdf(results):

    pdf_path = "report.pdf"

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    elements = []

    # Title
    elements.append(
        Paragraph(
            "Resume Screening Report",
            styles["Title"]
        )
    )

    # Date
    elements.append(
        Paragraph(
            f"Generated On: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 20))

    # Loop through results
    for result in results:

        # Resume name
        elements.append(
            Paragraph(
                f"Resume: {result['resume']}",
                styles["Heading2"]
            )
        )

        elements.append(Spacer(1, 8))

        # Final score
        elements.append(
            Paragraph(
                f"<b>Final Score:</b> {result['score']}%",
                styles["Normal"]
            )
        )

        # Rank label
        elements.append(
            Paragraph(
                f"<b>Rank:</b> {result['rank_label']}",
                styles["Normal"]
            )
        )

        elements.append(Spacer(1, 8))

        # Score breakdown
        elements.append(
            Paragraph(
                "<b>Score Breakdown:</b>",
                styles["Heading3"]
            )
        )

        elements.append(
            Paragraph(
                f"TF-IDF Score: {result['tfidf_score']}%",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"Keyword Score: {result['keyword_score']}%",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"Bonus Score: {result['bonus']}",
                styles["Normal"]
            )
        )

        elements.append(Spacer(1, 8))

        # Skills found
        skills_text = ", ".join(result["skills"])

        if not skills_text:
            skills_text = "No skills found"

        elements.append(
            Paragraph(
                "<b>Skills Found:</b>",
                styles["Heading3"]
            )
        )

        elements.append(
            Paragraph(
                skills_text,
                styles["Normal"]
            )
        )

        elements.append(Spacer(1, 8))

        # Missing skills
        missing_text = ", ".join(result["missing_skills"])

        if not missing_text:
            missing_text = "No missing skills"

        elements.append(
            Paragraph(
                "<b>Missing Skills:</b>",
                styles["Heading3"]
            )
        )

        elements.append(
            Paragraph(
                missing_text,
                styles["Normal"]
            )
        )

        elements.append(Spacer(1, 8))

        # Summary
        elements.append(
            Paragraph(
                "<b>Resume Summary:</b>",
                styles["Heading3"]
            )
        )

        elements.append(
            Paragraph(
                result["summary"],
                styles["Normal"]
            )
        )

        elements.append(Spacer(1, 25))

    # Build PDF
    doc.build(elements)

    return pdf_path