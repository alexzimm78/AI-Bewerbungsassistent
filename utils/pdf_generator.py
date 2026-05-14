from reportlab.pdfgen import canvas

USER_NAME = "Alexander Zimmermann"
EMAIL = "alexzimm@gmx.com"

def create_pdf(skills, experience, address):

    filename = "Lebenslauf.pdf"

    c = canvas.Canvas(filename)

    # Titel
    c.setFont("Helvetica-Bold", 24)
    c.drawString(180, 800, "Lebenslauf")

    c.line(80, 785, 520, 785)

    # Name
    c.setFont("Helvetica-Bold", 18)
    c.drawString(100, 740, USER_NAME)

    # Weiterbildung
    c.setFont("Helvetica", 13)
    c.drawString(100, 715, "AI Engineering Weiterbildung")

    # Kontakt
    c.setFont("Helvetica", 11)
    c.drawString(100, 690, f"E-Mail: {EMAIL}")
    c.drawString(100, 670, f"Adresse: {address}")

    # Erfahrung
    c.setFont("Helvetica-Bold", 15)
    c.drawString(100, 610, "Berufserfahrung")

    c.setFont("Helvetica", 12)
    c.drawString(120, 585, experience)

    # Skills
    c.setFont("Helvetica-Bold", 15)
    c.drawString(100, 530, "Kenntnisse")

    c.setFont("Helvetica", 12)
    c.drawString(120, 505, skills)

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(100, 100, "Erstellt mit AI Bewerbungsassistent")

    c.save()

    return filename