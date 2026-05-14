from telegram import Update
from telegram.ext import ContextTypes
from database.db import cursor


async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    cursor.execute("""
    SELECT skills, experience, address
    FROM users
    WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()

    if result:
        skills, experience, address = result
    else:
        skills = "Keine Skills"
        experience = "Keine Erfahrung"
        address = "Keine Adresse"

    text = f"""
👤 Dein Profil

✅ Skills:
{skills}

✅ Erfahrung:
{experience}

✅ Adresse:
{address}
"""

    await update.message.reply_text(text)