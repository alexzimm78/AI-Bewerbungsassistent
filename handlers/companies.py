from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db import conn, cursor


###

async def addcompany(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if len(args) < 2:
        await update.message.reply_text(
            "Benutzung:\n/addcompany Firmenname email@firma.de"
        )
        return

    name = args[0]
    email = args[1]
    user_id = update.effective_user.id

    cursor.execute("""
    INSERT INTO companies (user_id, name, email, status)
    VALUES (?, ?, ?, ?)
    """, (
        user_id,
        name,
        email,
        "gespeichert"
    ))

    conn.commit()

    await update.message.reply_text(
        f"✅ Firma gespeichert:\n{name}\n{email}"
    )

###
async def companies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    cursor.execute("""
    SELECT name, email, status
    FROM companies
    WHERE user_id = ?
    ORDER BY id DESC
    """, (user_id,))

    rows = cursor.fetchall()

    if not rows:
        await update.message.reply_text("❌ Keine Firmen gespeichert.")
        return

    text = "🏢 Deine Firmen\n\n"

    for i, row in enumerate(rows, start=1):
        name, email, status = row

        text += (
            f"{i}. {name}\n"
            f"📧 {email}\n"
            f"📌 Status: {status}\n\n"
        )

    await update.message.reply_text(text)
###
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if len(args) < 2:
        await update.message.reply_text(
            "Benutzung:\n/status Firmenname neuer_status\n\n"
            "Beispiel:\n/status Siemens eingeladen"
        )
        return

    company_name = args[0]
    new_status = " ".join(args[1:])
    user_id = update.effective_user.id

    cursor.execute("""
    UPDATE companies
    SET status = ?
    WHERE user_id = ? AND name = ?
    """, (
        new_status,
        user_id,
        company_name
    ))

    conn.commit()

    if cursor.rowcount == 0:
        await update.message.reply_text(
            f"❌ Firma nicht gefunden:\n{company_name}"
        )
        return

    await update.message.reply_text(
        f"✅ Status geändert:\n{company_name} → {new_status}"
    )

###
async def find(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if not args:
        await update.message.reply_text(
            "Benutzung:\n/find Firmenname"
        )
        return

    company_name = args[0]
    user_id = update.effective_user.id

    cursor.execute("""
    SELECT name, email, status
    FROM companies
    WHERE user_id = ? AND name LIKE ?
    """, (
        user_id,
        f"%{company_name}%"
    ))

    rows = cursor.fetchall()

    if not rows:
        await update.message.reply_text(
            f"❌ Keine Firma gefunden:\n{company_name}"
        )
        return

    text = "🔍 Suchergebnis\n\n"

    for row in rows:
        name, email, status = row

        text += (
            f"🏢 {name}\n"
            f"📧 {email}\n"
            f"📌 Status: {status}\n\n"
        )

    await update.message.reply_text(text)

###
async def deletecompany(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if not args:
        await update.message.reply_text(
            "Benutzung:\n/deletecompany Firmenname"
        )
        return

    company_name = args[0]
    user_id = update.effective_user.id

    cursor.execute("""
    DELETE FROM companies
    WHERE user_id = ? AND name = ?
    """, (
        user_id,
        company_name
    ))

    conn.commit()

    if cursor.rowcount == 0:
        await update.message.reply_text(
            f"❌ Firma nicht gefunden:\n{company_name}"
        )
        return

    await update.message.reply_text(
        f"🗑 Firma gelöscht:\n{company_name}"
    )

###
async def clearcompanies(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    cursor.execute("""
    DELETE FROM companies
    WHERE user_id = ?
    """, (user_id,))

    conn.commit()

    await update.message.reply_text(
        "🧹 Alle Firmen gelöscht."
    )
###
async def followup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if not args:
        await update.message.reply_text(
            "Benutzung:\n/followup Firmenname"
        )
        return

    company_name = args[0]
    user_id = update.effective_user.id

    cursor.execute("""
    SELECT name, email, status
    FROM companies
    WHERE user_id = ? AND name = ?
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

    name, email, status = company

    text = f"""
📩 Nachfassmail für {name}

An: {email}
Aktueller Status: {status}

-------------------------

Sehr geehrte Damen und Herren,

ich möchte mich höflich nach dem aktuellen Stand meiner Bewerbung erkundigen.

Ich habe Ihnen meine Bewerbungsunterlagen bereits zugesendet und bin weiterhin sehr an einer Mitarbeit in Ihrem Unternehmen interessiert.

Über eine kurze Rückmeldung würde ich mich sehr freuen.

Mit freundlichen Grüßen
Alexander Zimmermann
"""

    context.user_data["followup_email"] = email
    context.user_data["followup_subject"] = f"Nachfrage zu meiner Bewerbung bei {name}"
    context.user_data["followup_body"] = text

    keyboard = [
        [
            InlineKeyboardButton("✅ Nachfassmail senden", callback_data="confirm_followup"),
            InlineKeyboardButton("❌ Abbrechen", callback_data="cancel_followup"),
        ]
    ]

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

from utils.email_sender import send_email

###
async def followup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if not args:
        await update.message.reply_text(
            "Benutzung:\n/followup Firmenname"
        )
        return

    company_name = args[0]
    user_id = update.effective_user.id

    cursor.execute("""
    SELECT name, email, status
    FROM companies
    WHERE user_id = ? AND name = ?
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

    name, email, status = company

    body = f"""
Sehr geehrte Damen und Herren,

ich möchte mich höflich nach dem aktuellen Stand meiner Bewerbung erkundigen.

Ich habe Ihnen meine Bewerbungsunterlagen bereits zugesendet und bin weiterhin sehr an einer Mitarbeit in Ihrem Unternehmen interessiert.

Über eine kurze Rückmeldung würde ich mich sehr freuen.

Mit freundlichen Grüßen
Alexander Zimmermann
"""

    preview_text = f"""
📩 Nachfassmail für {name}

An: {email}
Aktueller Status: {status}

-------------------------

{body}
"""

    context.user_data["followup_email"] = email
    context.user_data["followup_subject"] = f"Nachfrage zu meiner Bewerbung bei {name}"
    context.user_data["followup_body"] = body

    keyboard = [
        [
            InlineKeyboardButton("✅ Nachfassmail senden", callback_data="confirm_followup"),
            InlineKeyboardButton("❌ Abbrechen", callback_data="cancel_followup"),
        ]
    ]

    await update.message.reply_text(
        preview_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

###
async def confirm_followup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    to_email = context.user_data.get("followup_email")
    subject = context.user_data.get("followup_subject")
    body = context.user_data.get("followup_body")

    if not to_email:
        await query.edit_message_text("❌ Keine Nachfassmail gefunden.")
        return

    try:
        send_email(
            to_email=to_email,
            subject=subject,
            body=body
        )

        cursor.execute("""
        UPDATE companies
        SET status = ?
        WHERE user_id = ? AND email = ?
        """, (
            "Nachfassmail gesendet",
            update.effective_user.id,
            to_email
        ))

        conn.commit()

        context.user_data["followup_email"] = None
        context.user_data["followup_subject"] = None
        context.user_data["followup_body"] = None

        await query.edit_message_text(
            f"✅ Nachfassmail gesendet an:\n{to_email}"
        )

    except Exception as e:
        await query.edit_message_text(
            f"❌ Fehler beim Senden:\n{e}"
        )

###
async def cancel_followup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data["followup_email"] = None
    context.user_data["followup_subject"] = None
    context.user_data["followup_body"] = None

    await query.edit_message_text("❌ Nachfassmail abgebrochen.")

###
async def companyinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    args = context.args

    if not args:
        await update.message.reply_text(
            "Benutzung:\n/companyinfo Firmenname"
        )
        return

    company_name = args[0]
    user_id = update.effective_user.id

    cursor.execute("""
    SELECT name, email, status
    FROM companies
    WHERE user_id = ? AND name = ?
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

    name, email, status = company

    cursor.execute("""
    SELECT COUNT(*)
    FROM interviews
    WHERE user_id = ?
    AND company = ?
    """, (
        user_id,
        name
    ))

    interview_count = cursor.fetchone()[0]

    text = (
        f"🏢 Firma\n\n"
        f"Name: {name}\n"
        f"📧 {email}\n\n"
        f"📌 Status:\n{status}\n\n"
        f"🎤 Interviews: {interview_count}"
    )

    await update.message.reply_text(text)

###