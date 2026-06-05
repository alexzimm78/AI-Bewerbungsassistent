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

    def count_status(status_name):
        cursor.execute("""
        SELECT COUNT(*)
        FROM companies
        WHERE user_id = ?
        AND status = ?
        """, (
            user_id,
            status_name
        ))

        return cursor.fetchone()[0]

    erstellt = count_status("Bewerbung erstellt")
    gesendet = count_status("Bewerbung gesendet")
    nachfass = count_status("Nachfassmail gesendet")
    interview = count_status("Interview")
    zusage = count_status("Zusage")
    absage = count_status("Absage")

    offen = erstellt + gesendet + nachfass

    if total > 0:
        erfolgsquote = round(
            ((interview + zusage) / total) * 100,
            1
        )
    else:
        erfolgsquote = 0

    text = (
        "📊 Bewerbungs Dashboard\n\n"
        f"🏢 Firmen gesamt: {total}\n\n"
        f"📝 Bewerbung erstellt: {erstellt}\n"
        f"📧 Bewerbung gesendet: {gesendet}\n"
        f"📬 Nachfassmail gesendet: {nachfass}\n"
        f"🎤 Interview: {interview}\n"
        f"✅ Zusage: {zusage}\n"
        f"❌ Absage: {absage}\n\n"
        f"⏳ Offen: {offen}\n"
        f"📈 Erfolgsquote: {erfolgsquote}%"
    )

    await update.message.reply_text(text)