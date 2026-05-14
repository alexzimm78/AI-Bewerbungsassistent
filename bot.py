from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

from dotenv import load_dotenv
import os

from handlers.start import start
from handlers.profile import profile
from handlers.pdf_handler import pdf
from handlers.bewerbung import bewerbung
from handlers.buttons import button
from handlers.messages import handle_message
from handlers.settings import setskills, setexperience, setaddress

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("setskills", setskills))
app.add_handler(CommandHandler("setexperience", setexperience))
app.add_handler(CommandHandler("setaddress", setaddress))
app.add_handler(CommandHandler("profile", profile))
app.add_handler(CommandHandler("bewerbung", bewerbung))
app.add_handler(CommandHandler("pdf", pdf))

app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🚀 Bot läuft...")

app.run_polling()