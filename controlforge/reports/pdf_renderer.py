from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)


def export_sections_to_pdf(
    sections: list,
    output_path,
    filename: str,
    chart_paths: list = None
):

    pdf_path = output_path / filename

    document = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    body_style = styles["BodyText"]

    story = []

    for index, section in enumerate(sections):

        if index == 0:
            story.append(
                Paragraph(
                    section["title"],
                    title_style
                )
            )
        else:
            story.append(
                Paragraph(
                    section["title"],
                    heading_style
                )
            )

        story.append(
            Spacer(1, 0.15 * inch)
        )

        content = section["content"].replace(
            "\n",
            "<br/>"
        )

        story.append(
            Paragraph(
                content,
                body_style
            )
        )

        story.append(
            Spacer(1, 0.25 * inch)
        )

    if chart_paths:

            story.append(
                Paragraph(
                    "Governance Analytics",
                    heading_style
                )
            )

            story.append(
                Spacer(1, 0.15 * inch)
            )

            for chart_path in chart_paths:

                story.append(
                    Image(
                        str(chart_path),
                        width=6.5 * inch,
                        height=4 * inch
                    )
                )

                story.append(
                    Spacer(1, 0.25 * inch)
                )   

    document.build(story)

    print("\nPDF report exported:")
    print(f"- {pdf_path}")