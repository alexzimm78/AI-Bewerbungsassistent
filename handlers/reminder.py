from telegram import Update
from telegram.ext import ContextTypes

from database.db import cursor


async def reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    cursor.execute("""
    SELECT name, status
    FROM companies
    WHERE user_id = ?
    """, (user_id,))

    companies = cursor.fetchall()

    if not companies:
        await update.message.reply_text("Keine Erinnerungen vorhanden.")
        return

    text = "🔔 Erinnerungen\n\n"
    found = False

    for name, status in companies:
        if status == "Interview":
            text += f"🎤 {name}\n→ Interview vorbereiten\n\n"
            found = True

        elif status == "Bewerbung gesendet":
            text += f"📧 {name}\n→ Nachfassmail im Blick behalten\n\n"
            found = True

        elif status == "Nachfassmail gesendet":
            text += f"📬 {name}\n→ Auf Rückmeldung warten\n\n"
            found = True

    if not found:
        text += "Keine dringenden Aktionen."

    await update.message.reply_text(text)