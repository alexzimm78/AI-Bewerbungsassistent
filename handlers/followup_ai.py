from telegram import Update
from telegram.ext import ContextTypes

from database.db import cursor
from utils.ai_generator import generate_followup_email


async def followupai(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    args = context.args

    if not args:
        await update.message.reply_text(
            "Benutzung:\n"
            "/followupai Firmenname"
        )
        return

    company_name = args[0]
    user_id = update.effective_user.id

    cursor.execute("""
    SELECT sent_at
    FROM companies
    WHERE user_id = ?
    AND name = ?
    """, (
        user_id,
        company_name
    ))

    company = cursor.fetchone()

    if not company:
        await update.message.reply_text(
            f"❌ Firma nicht gefunden:\n{company_name}"
        )
        return

    sent_at = company[0]

    text = f"""
Erstelle eine professionelle Nachfassmail.


Firma:
{company_name}

Bewerbung versendet:
{sent_at}

Der Bewerber heißt Alexander Zimmermann.

Die Mail soll freundlich, professionell und kurz sein.
- erwähne kein genaues Uhrzeitformat, nur das Datum
"""

    await update.message.reply_text(
        "🤖 Erstelle KI-Nachfassmail..."
    )

    result = generate_followup_email(
        company_name=company_name,
        sent_at=sent_at
    )

    await update.message.reply_text(result)