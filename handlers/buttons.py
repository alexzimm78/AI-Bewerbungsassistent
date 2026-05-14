from telegram import Update
from telegram.ext import ContextTypes


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    if query.data == "send":

        await query.edit_message_text(
            "✅ Bewerbung bereit zum Versand."
        )

    elif query.data == "edit":

        context.user_data["waiting_for_edit"] = True

        await query.edit_message_text(
            "✏️ Schreibe was geändert werden soll."
        )

    elif query.data == "cancel":

        await query.edit_message_text(
            "❌ Bewerbung abgebrochen."
        )