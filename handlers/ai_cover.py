from telegram import Update
from telegram.ext import ContextTypes

from database.db import conn, cursor
from utils.ai_generator import generate_ai_cover_letter


async def aibewerbung(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if not args:
        await update.message.reply_text(
            "📄 Bitte sende die Stellenanzeige hinter dem Befehl.\n\n"
            "Beispiel:\n/aibewerbung Siemens IT Support Microsoft 365 Service Desk"
        )
        return

    company_name = args[0]
    job_text = " ".join(args[1:])
    user_id = update.effective_user.id

    context.user_data["last_company_name"] = company_name

    cursor.execute("""
    SELECT skills, experience
    FROM users
    WHERE user_id = ?
    """, (user_id,))

    user = cursor.fetchone()

    if user:
        skills, experience = user
    else:
        skills = "Python, Microsoft 365, GitHub"
        experience = "Logistik, Kundenservice, strukturierte Arbeitsweise"

    await update.message.reply_text("🤖 Erstelle individuelles Anschreiben...")

    result = generate_ai_cover_letter(
        job_text=job_text,
        skills=skills,
        experience=experience
    )
    context.user_data["last_cover_letter"] = result
    # Firma im CRM speichern oder aktualisieren
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
        SET status = ?
        WHERE user_id = ?
        AND name = ?
        """, (
            "Bewerbung erstellt",
            user_id,
            company_name
        ))
    else:
        cursor.execute("""
        INSERT INTO companies (
            user_id,
            name,
            email,
            status
        )
        VALUES (?, ?, ?, ?)
        """, (
            user_id,
            company_name,
            "Noch keine Email",
            "Bewerbung erstellt"
        ))

    conn.commit()