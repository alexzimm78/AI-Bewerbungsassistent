from telegram import Update
from telegram.ext import ContextTypes

from datetime import datetime

from database.db import conn, cursor
from utils.ai_generator import generate_ai_cover_letter
from utils.pdf_generator import create_cover_pdf
from utils.email_sender import send_email


async def autoapply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if len(args) < 3:
        await update.message.reply_text(
            "Benutzung:\n"
            "/autoapply Firma email@firma.de Stellenanzeige\n\n"
            "Beispiel:\n"
            "/autoapply Vivantes karriere@vivantes.de Applikationsbetreuer Logistische Systeme"
        )
        return

    company_name = args[0]
    to_email = args[1]
    job_text = " ".join(args[2:])
    user_id = update.effective_user.id

    await update.message.reply_text("🤖 Erstelle Anschreiben...")

    cursor.execute("""
    SELECT skills, experience
    FROM users
    WHERE user_id = ?
    """, (user_id,))

    user = cursor.fetchone()

    if user:
        skills, experience = user
    else:
        skills = "Python, Microsoft 365, GitHub, SQLite"
        experience = "Logistik, Kundenservice, strukturierte Arbeitsweise"

    cover_letter = generate_ai_cover_letter(
        job_text=job_text,
        skills=skills,
        experience=experience
    )

    context.user_data["last_cover_letter"] = cover_letter
    context.user_data["last_company_name"] = company_name

    await update.message.reply_text("📄 Erstelle PDF...")

    cover_pdf = create_cover_pdf(
        cover_letter,
        filename=f"Bewerbung_{company_name}.pdf"
    )

    lebenslauf_pdf = "Lebenslauf.pdf"

    subject = f"Bewerbung als {job_text[:60]}"

    body = f"""
Sehr geehrte Damen und Herren,

anbei übersende ich Ihnen meine Bewerbungsunterlagen.

Über die Möglichkeit eines persönlichen Gesprächs freue ich mich sehr.

Mit freundlichen Grüßen
Alexander Zimmermann
"""

    await update.message.reply_text("📧 Sende Bewerbung...")

    send_email(
        to_email=to_email,
        subject=subject,
        body=body,
        attachments=[
            cover_pdf,
            lebenslauf_pdf
        ]
    )

    sent_at = datetime.now().strftime("%d.%m.%Y %H:%M")

    cursor.execute("""
    SELECT id
    FROM companies
    WHERE user_id = ?
    AND name = ?
    """, (
        user_id,
        company_name
    ))

    existing_company = cursor.fetchone()

    if existing_company:
        cursor.execute("""
        UPDATE companies
        SET email = ?,
            status = ?,
            sent_at = ?
        WHERE user_id = ?
        AND name = ?
        """, (
            to_email,
            "Bewerbung gesendet",
            sent_at,
            user_id,
            company_name
        ))
    else:
        cursor.execute("""
        INSERT INTO companies (
            user_id,
            name,
            email,
            status,
            sent_at
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            user_id,
            company_name,
            to_email,
            "Bewerbung gesendet",
            sent_at
        ))

    conn.commit()

    await update.message.reply_document(
        document=open(cover_pdf, "rb")
    )

    await update.message.reply_text(
        f"✅ AutoApply abgeschlossen\n\n"
        f"🏢 Firma: {company_name}\n"
        f"📧 Email: {to_email}\n"
        f"📄 PDF: {cover_pdf}\n"
        f"📅 Gesendet: {sent_at}"
    )