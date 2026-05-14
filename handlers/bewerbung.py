from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database.db import cursor

USER_NAME = "Alexander Zimmermann"


async def bewerbung(update: Update, context: ContextTypes.DEFAULT_TYPE):

    job_title = " ".join(context.args)

    if not job_title:
        await update.message.reply_text(
            "Benutzung:\n/bewerbung IT Support"
        )
        return

    user_id = update.effective_user.id

    cursor.execute("""
    SELECT skills, experience
    FROM users
    WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()

    if result:
        skills, experience = result[:2]
    else:
        skills = "Teamfähigkeit"
        experience = "Logistik"

    text = f"""
Hallo,

hiermit möchte ich mich auf die Stelle als {job_title} bewerben.

Ich interessiere mich sehr für IT und absolviere aktuell eine Weiterbildung im Bereich AI Engineering.

Durch meine bisherigen Erfahrungen in den Bereichen {experience}
bringe ich Zuverlässigkeit, strukturiertes Arbeiten und Verantwortungsbewusstsein mit.

Zusätzlich verfüge ich über folgende Kenntnisse und Fähigkeiten:
{skills}

Mit freundlichen Grüßen
{USER_NAME}
"""

    keyboard = [
        [
            InlineKeyboardButton("✅ Отправить", callback_data="send"),
            InlineKeyboardButton("✏️ Изменить", callback_data="edit"),
        ],
        [InlineKeyboardButton("❌ Отмена", callback_data="cancel")]
    ]

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )