from telegram import Update
from telegram.ext import ContextTypes

from database.db import cursor


async def kanban(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    statuses = [
        "Bewerbung erstellt",
        "Bewerbung gesendet",
        "Nachfassmail gesendet",
        "Interview",
        "Zusage",
        "Absage"
    ]

    emojis = {
        "Bewerbung erstellt": "📝",
        "Bewerbung gesendet": "📧",
        "Nachfassmail gesendet": "📬",
        "Interview": "🎤",
        "Zusage": "✅",
        "Absage": "❌"
    }

    text = "📋 Bewerbungs Kanban Board\n\n"

    for status in statuses:

        cursor.execute("""
        SELECT name
        FROM companies
        WHERE user_id = ?
        AND status = ?
        ORDER BY name
        """, (
            user_id,
            status
        ))

        companies = cursor.fetchall()

        count = len(companies)

        text += f"{emojis[status]} {status} ({count})\n"

        if companies:
            for company in companies:
                text += f"- {company[0]}\n"
        else:
            text += "-\n"

        text += "\n"

    await update.message.reply_text(text)