from telegram import Update
from telegram.ext import ContextTypes

from database.db import cursor
from utils.pdf_generator import create_cover_pdf


async def pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):

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

    filename = create_pdf(
        skills,
        experience,
        address
    )

    await update.message.reply_document(
        document=open(filename, "rb")
    )