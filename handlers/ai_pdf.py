from telegram import Update
from telegram.ext import ContextTypes

from utils.pdf_generator import create_cover_pdf


async def aipdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cover_letter = context.user_data.get("last_cover_letter")

    if not cover_letter:
        await update.message.reply_text(
            "❌ Kein Anschreiben gefunden.\n\n"
            "Erstelle zuerst eins mit:\n"
            "/aibewerbung Stellenanzeige"
        )
        return

    company_name = context.user_data.get(
        "last_company_name",
        "Firma"
    )

    filename = create_cover_pdf(
        cover_letter,
        filename=f"Bewerbung_{company_name}.pdf"
    )

    await update.message.reply_document(
        document=open(filename, "rb")
    )