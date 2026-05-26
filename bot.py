from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

from dotenv import load_dotenv
import os

from handlers.start import start, help_command
from handlers.profile import profile
from handlers.pdf_handler import pdf
from handlers.bewerbung import bewerbung
from handlers.buttons import button
from handlers.messages import handle_message
from handlers.settings import setskills, setexperience, setaddress
from handlers.email_handler import (
    sendtest,
    sendbewerbung,
    confirm_sendbewerbung,
    cancel_sendbewerbung,
    history,
    stats,
    clearhistory,
    export
)
from handlers.companies import (
    addcompany,
    companies,
    status,
    find,
    deletecompany,
    clearcompanies,
    followup,
    confirm_followup,
    cancel_followup,
    companyinfo
)
from handlers.interviews import interview, interviews, reminders, deleteinterview
from handlers.dashboard import dashboard


load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

app = ApplicationBuilder().token(TOKEN).build()
###

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("setskills", setskills))
app.add_handler(CommandHandler("setexperience", setexperience))
app.add_handler(CommandHandler("setaddress", setaddress))
app.add_handler(CommandHandler("profile", profile))
app.add_handler(CommandHandler("bewerbung", bewerbung))
app.add_handler(CommandHandler("pdf", pdf))
app.add_handler(CommandHandler("sendbewerbung", sendbewerbung))
app.add_handler(CommandHandler("sendtest", sendtest))
app.add_handler(CommandHandler("history", history))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(CommandHandler("addcompany", addcompany))
app.add_handler(CommandHandler("companies", companies))
app.add_handler(CommandHandler("status", status))
app.add_handler(CommandHandler("find", find))
app.add_handler(CommandHandler("interview", interview))
app.add_handler(CommandHandler("interviews", interviews))
app.add_handler(CommandHandler("reminders", reminders))
app.add_handler(CommandHandler("deletecompany", deletecompany))
app.add_handler(CommandHandler("deleteinterview", deleteinterview))
app.add_handler(CommandHandler("clearhistory", clearhistory))
app.add_handler(CommandHandler("clearcompanies", clearcompanies))
app.add_handler(CommandHandler("export", export))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("dashboard", dashboard))
app.add_handler(CommandHandler("followup", followup))
app.add_handler(CommandHandler("companyinfo", companyinfo)
)





###
app.add_handler(CallbackQueryHandler(confirm_sendbewerbung, pattern="confirm_send_email"))
app.add_handler(CallbackQueryHandler(cancel_sendbewerbung, pattern="cancel_send_email"))
app.add_handler(CallbackQueryHandler(confirm_followup, pattern="confirm_followup"))
app.add_handler(CallbackQueryHandler(cancel_followup, pattern="cancel_followup"))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🚀 Bot läuft...")

app.run_polling()