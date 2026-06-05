from telegram import Update
from telegram.ext import ContextTypes

from database.db import cursor
from datetime import datetime


async def priority(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    cursor.execute("""
    SELECT name, status, sent_at
    FROM companies
    WHERE user_id = ?
    """, (user_id,))

    companies = cursor.fetchall()

    interview = []
    followup = []
    waiting = []

    for company, status, sent_at in companies:

        if status == "Interview":
            interview.append(company)

        elif status == "Bewerbung gesendet":

            if sent_at:

                try:

                    sent_date = datetime.strptime(
                        sent_at,
                        "%d.%m.%Y %H:%M"
                    )

                    days = (
                            datetime.now() - sent_date
                    ).days

                except:
                    days = 0

            else:
                days = 0

            followup.append(
                (
                    company,
                    days
                )
            )

        elif status == "Nachfassmail gesendet":
            waiting.append(company)

    text = "🔥 Priorität heute\n\n"

    number = 1

    for company in interview:
        text += (
            f"{number}️⃣ {company}\n"
            f"🎤 Interview vorbereiten\n\n"
        )
        number += 1

    for company, days in followup:
        if days >= 7:

            text += (
                f"{number}️⃣ {company}\n"
                f"📅 Vor {days} Tagen versendet\n"
                f"🚨 Nachfassmail senden\n\n"
            )


        else:

            text += (
                f"{number}️⃣ {company}\n"
                f"📅 Vor {days} Tagen versendet\n"
                f"⏳ Noch warten\n\n"
            )
        number += 1

    for company in waiting:
        text += (
            f"{number}️⃣ {company}\n"
            f"⏳ Auf Rückmeldung warten\n\n"
        )
        number += 1

    if number == 1:
        text += "Keine offenen Aktionen."

    await update.message.reply_text(text)