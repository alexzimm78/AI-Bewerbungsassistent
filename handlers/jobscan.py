from telegram import Update
from telegram.ext import ContextTypes

from utils.ai_generator import generate_job_analysis


async def jobscan(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    args = context.args

    if not args:
        await update.message.reply_text(
            "Benutzung:\n"
            "/jobscan Stellenanzeige"
        )
        return

    job_text = " ".join(args)

    await update.message.reply_text(
        "🤖 Analysiere Stellenanzeige..."
    )

    result = generate_job_analysis(job_text)

    await update.message.reply_text(result)