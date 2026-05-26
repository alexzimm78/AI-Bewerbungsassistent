from telegram import Update
from telegram.ext import ContextTypes

from database.db import conn, cursor

###
async def interview(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if len(args) < 3:
        await update.message.reply_text(
            "Benutzung:\n/interview Firma Datum Uhrzeit\n\n"
            "Beispiel:\n/interview Siemens 20.05.2026 14:00"
        )
        return

    company = args[0]
    interview_date = args[1] + " " + args[2]
    note = " ".join(args[3:]) if len(args) > 3 else ""
    user_id = update.effective_user.id

    cursor.execute("""
    INSERT INTO interviews (user_id, company, interview_date, note)
    VALUES (?, ?, ?, ?)
    """, (
        user_id,
        company,
        interview_date,
        note
    ))

    conn.commit()

    await update.message.reply_text(
        f"✅ Interview gespeichert:\n{company}\n📅 {interview_date}"
    )

###
async def interviews(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    cursor.execute("""
    SELECT company, interview_date, note
    FROM interviews
    WHERE user_id = ?
    ORDER BY id DESC
    """, (user_id,))

    rows = cursor.fetchall()

    if not rows:
        await update.message.reply_text("❌ Keine Interviews gespeichert.")
        return

    text = "📅 Deine Interviews\n\n"

    for i, row in enumerate(rows, start=1):
        company, interview_date, note = row

        text += (
            f"{i}. 🏢 {company}\n"
            f"📅 {interview_date}\n"
        )

        if note:
            text += f"📝 {note}\n"

        text += "\n"

    await update.message.reply_text(text)

from datetime import datetime

###
async def reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    cursor.execute("""
    SELECT company, interview_date, note
    FROM interviews
    WHERE user_id = ?
    ORDER BY id ASC
    """, (user_id,))

    rows = cursor.fetchall()

    if not rows:
        await update.message.reply_text(
            "❌ Keine Interviews gefunden."
        )
        return

    text = "🔔 Kommende Interviews\n\n"

    now = datetime.now()

    for row in rows:

        company, interview_date, note = row

        try:
            interview_dt = datetime.strptime(
                interview_date,
                "%d.%m.%Y %H:%M"
            )

            diff = interview_dt - now
            days_left = diff.days

            if days_left >= 0:

                text += (
                    f"🏢 {company}\n"
                    f"📅 {interview_date}\n"
                    f"⏳ in {days_left} Tagen\n"
                )

                if note:
                    text += f"📝 {note}\n"

                text += "\n"

        except:
            continue

    await update.message.reply_text(text)
###
async def deleteinterview(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if not args:
        await update.message.reply_text(
            "Benutzung:\n/deleteinterview Firmenname"
        )
        return

    company = args[0]
    user_id = update.effective_user.id

    cursor.execute("""
    DELETE FROM interviews
    WHERE user_id = ? AND company = ?
    """, (
        user_id,
        company
    ))

    conn.commit()

    if cursor.rowcount == 0:
        await update.message.reply_text(
            f"❌ Interview nicht gefunden:\n{company}"
        )
        return

    await update.message.reply_text(
        f"🗑 Interview gelöscht:\n{company}"
    )

###
