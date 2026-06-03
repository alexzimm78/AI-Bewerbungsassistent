from telegram import Update
from telegram.ext import ContextTypes


async def pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📄 Für PDF bitte zuerst ein Anschreiben erstellen:\n\n"
        "/aibewerbung Firma Stellenanzeige\n\n"
        "Danach:\n"
        "/aipdf"
    )