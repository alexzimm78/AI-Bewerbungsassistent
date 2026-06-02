from telegram import Update
from telegram.ext import ContextTypes

from database.db import cursor


async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    cursor.execute("""
    SELECT COUNT(*)
    FROM companies
    WHERE user_id = ?
    """, (user_id,))

    total = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM companies
    WHERE user_id = ?
    AND status = 'Bewerbung erstellt'
    """, (user_id,))

    erstellt = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM companies
    WHERE user_id = ?
    AND status = 'Bewerbung gesendet'
    """, (user_id,))

    gesendet = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM companies
    WHERE user_id = ?
    AND status = 'Nachfassmail gesendet'
    """, (user_id,))

    nachfass = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM companies
    WHERE user_id = ?
    AND status = 'Interview'
    """, (user_id,))

    interviews_status = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM companies
    WHERE user_id = ?
    AND status = 'Zusage'
    """, (user_id,))

    zusagen = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM companies
    WHERE user_id = ?
    AND status = 'Absage'
    """, (user_id,))

    absagen = cursor.fetchone()[0]

    offen = erstellt + gesendet + nachfass

    if total > 0:
        erfolgsquote = round(
            ((interviews_status + zusagen) / total) * 100,
            1
        )
    else:
        erfolgsquote = 0

    text = (
        "📊 Bewerbungs Dashboard\n\n"
        f"📨 Firmen gesamt: {total}\n\n"
        f"📝 Erstellt: {erstellt}\n"
        f"📤 Gesendet: {gesendet}\n"
        f"📩 Nachfassmail: {nachfass}\n"
        f"🎤 Interview: {interviews_status}\n"
        f"✅ Zusagen: {zusagen}\n"
        f"❌ Absagen: {absagen}\n"
        f"⏳ Offen: {offen}\n\n"
        f"📈 Erfolgsquote: {erfolgsquote}%"
    )

    await update.message.reply_text(text)