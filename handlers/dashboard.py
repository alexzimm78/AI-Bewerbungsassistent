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
    AND status = 'eingeladen'
    """, (user_id,))

    eingeladen = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM interviews
    WHERE user_id = ?
    """, (user_id,))

    interviews = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM companies
    WHERE user_id = ?
    AND status = 'absage'
    """, (user_id,))

    absagen = cursor.fetchone()[0]

    offen = total - eingeladen - absagen

    if total > 0:
        erfolgsquote = round(
            (eingeladen / total) * 100,
            1
        )
    else:
        erfolgsquote = 0
    text = (
        "📊 Bewerbungs Dashboard\n\n"
        f"📨 Bewerbungen: {total}\n"
        f"✅ Eingeladen: {eingeladen}\n"
        f"🎤 Interviews: {interviews}\n"
        f"❌ Absagen: {absagen}\n"
        f"⏳ Offen: {offen}\n\n"
        f"📈 Erfolgsquote: {erfolgsquote}%"
    )


    await update.message.reply_text(text)