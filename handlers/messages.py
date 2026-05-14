from telegram import Update
from telegram.ext import ContextTypes


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text

    if context.user_data.get("waiting_for_edit"):

        new_text = f"""
✏️ Änderung gespeichert:

{user_text}
"""

        context.user_data["waiting_for_edit"] = False

        await update.message.reply_text(new_text)