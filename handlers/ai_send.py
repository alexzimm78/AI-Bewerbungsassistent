from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from utils.email_sender import send_email
from database.db import conn, cursor


async def sendai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if len(args) < 2:
        await update.message.reply_text(
            "Benutzung:\n"
            "/sendai Firma email@firma.de\n\n"
            "Beispiel:\n"
            "/sendai Vivantes karriere@vivantes.de"
        )
        return

    company_name = args[0]
    to_email = args[1]

    cover_pdf = f"bewerbungen/Bewerbung_{company_name}.pdf"
    lebenslauf_pdf = "Lebenslauf.pdf"

    context.user_data["sendai_company"] = company_name
    context.user_data["sendai_email"] = to_email
    context.user_data["sendai_cover_pdf"] = cover_pdf
    context.user_data["sendai_lebenslauf_pdf"] = lebenslauf_pdf

    keyboard = [
        [
            InlineKeyboardButton("✅ Bewerbung senden", callback_data="confirm_sendai"),
            InlineKeyboardButton("❌ Abbrechen", callback_data="cancel_sendai"),
        ]
    ]

    await update.message.reply_text(
        f"📧 Bewerbung senden?\n\n"
        f"🏢 Firma: {company_name}\n"
        f"📨 An: {to_email}\n\n"
        f"📎 Anhänge:\n"
        f"- {cover_pdf}\n"
        f"- {lebenslauf_pdf}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def confirm_sendai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    company_name = context.user_data.get("sendai_company")
    to_email = context.user_data.get("sendai_email")
    cover_pdf = context.user_data.get("sendai_cover_pdf")
    lebenslauf_pdf = context.user_data.get("sendai_lebenslauf_pdf")

    if not company_name or not to_email:
        await query.edit_message_text("❌ Keine Bewerbung zum Senden gefunden.")
        return

    subject = f"Bewerbung bei {company_name}"

    body = f"""
Sehr geehrte Damen und Herren,

anbei übersende ich Ihnen meine Bewerbungsunterlagen.

Über die Möglichkeit eines persönlichen Gesprächs freue ich mich sehr.

Mit freundlichen Grüßen
Alexander Zimmermann
"""

    try:
        send_email(
            to_email=to_email,
            subject=subject,
            body=body,
            attachments=[
                cover_pdf,
                lebenslauf_pdf
            ]
        )

        cursor.execute("""
        UPDATE companies
        SET email = ?, status = ?
        WHERE name = ?
        """, (
            to_email,
            "Bewerbung gesendet",
            company_name
        ))

        conn.commit()

        await query.edit_message_text(
            f"✅ Bewerbung wurde gesendet an:\n{to_email}"
        )

    except Exception as e:
        await query.edit_message_text(
            f"❌ Fehler beim Senden:\n{e}"
        )


async def cancel_sendai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text("❌ Versand abgebrochen.")