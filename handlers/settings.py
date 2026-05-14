from telegram import Update
from telegram.ext import ContextTypes

from database.db import conn, cursor


async def setskills(update: Update, context: ContextTypes.DEFAULT_TYPE):
    skills = " ".join(context.args)

    if not skills:
        await update.message.reply_text("Benutzung:\n/setskills Python, SAP")
        return

    user_id = update.effective_user.id

    cursor.execute("""
    INSERT OR REPLACE INTO users (user_id, skills)
    VALUES (?, ?)
    """, (user_id, skills))

    conn.commit()

    await update.message.reply_text(f"✅ Skills gespeichert:\n{skills}")


async def setexperience(update: Update, context: ContextTypes.DEFAULT_TYPE):
    experience = " ".join(context.args)

    if not experience:
        await update.message.reply_text("Benutzung:\n/setexperience Logistik, Fahrer")
        return

    user_id = update.effective_user.id

    cursor.execute("""
    UPDATE users
    SET experience = ?
    WHERE user_id = ?
    """, (experience, user_id))

    conn.commit()

    await update.message.reply_text(f"✅ Erfahrung gespeichert:\n{experience}")


async def setaddress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    address = " ".join(context.args)

    if not address:
        await update.message.reply_text("Benutzung:\n/setaddress Rhinstr.1, 10315 Berlin")
        return

    user_id = update.effective_user.id

    cursor.execute("""
    UPDATE users
    SET address = ?
    WHERE user_id = ?
    """, (address, user_id))

    conn.commit()

    await update.message.reply_text(f"✅ Adresse gespeichert:\n{address}")