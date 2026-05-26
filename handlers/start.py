from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Willkommen beim AI Bewerbungsassistent."
    )
###
async def help_command(update, context):
    text = """
🤖 AI Bewerbungsassistent — Befehle

📄 Bewerbung:
 /bewerbung IT Support
 /sendbewerbung sap email@firma.de
 /history
 /stats
 /export

🏢 Firmen:
 /addcompany Siemens jobs@siemens.de
 /companies
 /find Siemens
 /status Siemens eingeladen
 /deletecompany Siemens
 /clearcompanies

📅 Interviews:
 /interview Siemens 20.05.2026 14:00 Teams
 /interviews
 /reminders
 /deleteinterview Siemens

👤 Profil:
 /profile
 /setskills Python, SAP
 /setexperience Logistik, Fahrer
 /setaddress Straße 1, 10315 Berlin

🧪 Test:
 /sendtest
"""

    await update.message.reply_text(text)