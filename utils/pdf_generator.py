import os
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


def create_cover_pdf(text, filename=None):
    if filename is None:
        date = datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"Bewerbung_{date}.pdf"

    folder = "bewerbungen"
    os.makedirs(folder, exist_ok=True)

    filepath = os.path.join(folder, filename)

    doc = SimpleDocTemplate(filepath)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("<b>Alexander Zimmermann</b>", styles["Title"]))
    content.append(Paragraph("Berlin | alexzimm@gmx.com", styles["Normal"]))
    content.append(Spacer(1, 25))

    content.append(Paragraph("<b>Bewerbung</b>", styles["Heading2"]))
    content.append(Spacer(1, 10))

    for p in text.split("\n"):
        if p.strip():
            content.append(Paragraph(p, styles["Normal"]))
            content.append(Spacer(1, 8))

    doc.build(content)

    return filepath