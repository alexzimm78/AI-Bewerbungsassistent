from telegram import Update
from telegram.ext import ContextTypes

from database.db import cursor
from utils.ai_generator import generate_ai_cover_letter


async def aibewerbung(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if not args:
        await update.message.reply_text(
            "📄 Bitte sende die Stellenanzeige hinter dem Befehl.\n\n"
            "Beispiel:\n/aibewerbung IT Support Microsoft 365 Service Desk"
        )
        return

    job_text = " ".join(args)
    user_id = update.effective_user.id

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

    await update.message.reply_text(result)