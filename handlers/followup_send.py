from telegram import Update
from telegram.ext import ContextTypes

from database.db import conn, cursor
from utils.email_sender import send_email
from utils.ai_generator import generate_followup_email


async def followupsend(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    args = context.args

    if not args:
        await update.message.reply_text(
            "Benutzung:\n"
            "/followupsend Firmenname"
        )
        return

    company_name = args[0]
    user_id = update.effective_user.id

    cursor.execute("""
    SELECT email, sent_at
    FROM companies
    WHERE user_id = ?
    AND name = ?
    """, (
        user_id,
        company_name
    ))

    company = cursor.fetchone()

    if not company:
        await update.message.reply_text(
            f"❌ Firma nicht gefunden:\n{company_name}"
        )
        return

    email, sent_at = company

    await update.message.reply_text(
        "🤖 Erstelle Nachfassmail..."
    )

    mail_text = generate_followup_email(
        company_name=company_name,
        sent_at=sent_at
    )

    lines = mail_text.split("\n")

    subject = "Nachfrage zum Stand meiner Bewerbung"

    if lines and lines[0].lower().startswith("betreff"):
        subject = lines[0].replace("Betreff:", "").strip()
        mail_text = "\n".join(lines[1:]).strip()

    await update.message.reply_text(
        "📧 Versende Nachfassmail..."
    )

    send_email(
        to_email=email,
        subject=subject,
        body=mail_text
    )

    cursor.execute("""
    UPDATE companies
    SET status = ?
    WHERE user_id = ?
    AND name = ?
    """, (
        "Nachfassmail gesendet",
        user_id,
        company_name
    ))

    conn.commit()

    await update.message.reply_text(
        f"✅ Nachfassmail versendet\n\n"
        f"🏢 Firma: {company_name}\n"
        f"📧 Email: {email}"
    )