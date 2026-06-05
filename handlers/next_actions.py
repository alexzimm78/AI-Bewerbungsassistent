from telegram import Update
from telegram.ext import ContextTypes

from database.db import cursor


async def next_actions(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    cursor.execute("""
    SELECT name, status
    FROM companies
    WHERE user_id = ?
    ORDER BY name
    """, (user_id,))

    companies = cursor.fetchall()

    if not companies:
        await update.message.reply_text(
            "Keine Firmen vorhanden."
        )
        return

    text = "📌 Nächste Aktionen\n\n"

    for company, status in companies:

        text += f"🏢 {company}\n"

        if status == "Bewerbung erstellt":
            text += "→ Bewerbung versenden\n"

        elif status == "Bewerbung gesendet":
            text += "→ In einigen Tagen nachfassen\n"

        elif status == "Nachfassmail gesendet":
            text += "→ Auf Rückmeldung warten\n"

        elif status == "Interview":
            text += "→ Interview vorbereiten\n"

        elif status == "Zusage":
            text += "→ Vertragsdetails prüfen\n"

        elif status == "Absage":
            text += "→ Neue Bewerbung senden\n"

        text += "\n"

    await update.message.reply_text(text)