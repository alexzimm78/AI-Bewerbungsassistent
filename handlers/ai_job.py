from telegram import Update
from telegram.ext import ContextTypes

from utils.ai_generator import analyze_job


async def aijob(update: Update, context: ContextTypes.DEFAULT_TYPE):

    args = context.args

    if not args:
        await update.message.reply_text(
            "📄 Bitte sende die Stellenanzeige hinter dem Befehl.\n\n"
            "Beispiel:\n"
            "/aijob IT Support Microsoft 365 Service Desk"
        )
        return

    job_text = " ".join(args)

    await update.message.reply_text(
        "🤖 Analysiere Stellenanzeige..."
    )

    result = analyze_job(job_text)

    await update.message.reply_text(result)