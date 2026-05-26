from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from utils.email_sender import send_email
from database.db import conn, cursor

from datetime import datetime


def get_profile(user_id):
    cursor.execute("""
    SELECT skills, experience, address
    FROM users
    WHERE user_id = ?
    """, (user_id,))

    user = cursor.fetchone()

    if user:
        skills, experience, address = user
    else:
        skills = "Nicht angegeben"
        experience = "Nicht angegeben"
        address = "Nicht angegeben"

    return skills, experience, address

def get_bewerbung_text(
    bewerbung_typ,
    skills,
    experience,
    company_name
):

    if bewerbung_typ == "support":

        subject = "Bewerbung als IT Support Mitarbeiter"

        body = f"""
Sehr geehrte Damen und Herren bei {company_name},

mit großem Interesse bewerbe ich mich auf die Position als IT Support Mitarbeiter.

Aktuell absolviere ich eine Weiterbildung zum AI Engineer an der AIT Technology School. Dabei erweitere ich meine Kenntnisse in Python, Datenanalyse, Automatisierung und modernen IT-Technologien.

Durch meine langjährige Tätigkeit in der Logistik habe ich gelernt, strukturiert, zuverlässig und lösungsorientiert zu arbeiten. Die Zusammenarbeit mit Kunden und verschiedenen Ansprechpartnern hat meine Serviceorientierung und Kommunikationsfähigkeit gestärkt.

Zusätzlich arbeite ich an eigenen IT-Projekten und konnte praktische Erfahrungen mit Python, SQLite, GitHub und der Entwicklung eines Telegram-basierten Bewerbungsassistenten sammeln.

Ich freue mich darauf, meine Motivation und Lernbereitschaft in Ihrem Unternehmen einzubringen.

Mit freundlichen Grüßen

Alexander Zimmermann
"""

    elif bewerbung_typ == "servicedesk":

        subject = "Bewerbung als Service Desk Mitarbeiter"

        body = f"""
Sehr geehrte Damen und Herren bei {company_name},

mit großem Interesse bewerbe ich mich auf die Position im Service Desk.

Aktuell absolviere ich eine Weiterbildung zum AI Engineer und erweitere kontinuierlich meine Kenntnisse im IT-Bereich.

In meiner bisherigen Tätigkeit habe ich gelernt, serviceorientiert zu arbeiten, Probleme strukturiert zu lösen und auch in stressigen Situationen den Überblick zu behalten.

Besonders reizt mich die Möglichkeit, Anwender bei technischen Fragestellungen zu unterstützen und gemeinsam Lösungen zu finden.

Ich freue mich darauf, mich in Ihrem Unternehmen weiterzuentwickeln.

Mit freundlichen Grüßen

Alexander Zimmermann
"""

    elif bewerbung_typ == "application":

        subject = "Bewerbung als Applikationsbetreuer"

        body = f"""
Sehr geehrte Damen und Herren bei {company_name},

mit großem Interesse bewerbe ich mich als Applikationsbetreuer.

Durch meine langjährige Erfahrung in der Logistik verfüge ich über ein gutes Verständnis für betriebliche Prozesse. Aktuell erweitere ich mein Wissen durch eine Weiterbildung zum AI Engineer.

Besonders interessiert mich die Schnittstelle zwischen Fachbereichen und IT. Die Betreuung von Anwendungen, die Unterstützung von Anwendern sowie die Optimierung von Prozessen entsprechen genau meinen Interessen.

Zusätzlich arbeite ich an eigenen Python-Projekten und sammle praktische Erfahrungen in den Bereichen Datenbanken, Automatisierung und Softwareentwicklung.

Über die Möglichkeit, mich persönlich vorzustellen, freue ich mich sehr.

Mit freundlichen Grüßen

Alexander Zimmermann
"""

    else:

        subject = "Bewerbung"

        body = f"""
Sehr geehrte Damen und Herren bei {company_name},

hiermit bewerbe ich mich bei Ihnen.

Mit freundlichen Grüßen

Alexander Zimmermann
"""

    return subject, body


async def sendtest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        send_email(
            to_email="alexzimm@gmx.com",
            subject="Test vom Telegram Bot",
            body="Hallo Alexander, diese Email wurde direkt vom Telegram Bot gesendet."
        )
        await update.message.reply_text("✅ Test-Email wurde gesendet.")
    except Exception as e:
        await update.message.reply_text(f"❌ Fehler beim Senden:\n{e}")


async def sendbewerbung(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if len(args) < 3:
        await update.message.reply_text(
            "Benutzung:\n/sendbewerbung typ email\n\n"
            "Beispiele:\n"
            "/sendbewerbung sap firma@email.de\n"
            "/sendbewerbung support firma@email.de\n"
            "/sendbewerbung it firma@email.de"
        )
        return

    bewerbung_typ = args[0].lower()
    to_email = args[1]
    company_name = args[2]
    context.user_data["company_name"] = company_name
    user_id = update.effective_user.id

    skills, experience, address = get_profile(user_id)
    subject, body = get_bewerbung_text(
        bewerbung_typ,
        skills,
        experience,
        company_name
    )

    context.user_data["pending_email"] = to_email
    context.user_data["bewerbung_typ"] = bewerbung_typ
    context.user_data["pending_subject"] = subject
    context.user_data["pending_body"] = body

    keyboard = [
        [
            InlineKeyboardButton("✅ Ja senden", callback_data="confirm_send_email"),
            InlineKeyboardButton("❌ Abbrechen", callback_data="cancel_send_email"),
        ]
    ]

    await update.message.reply_text(
        f"""
📧 Bewerbung Vorschau

👤 Typ: {bewerbung_typ}
📨 Email: {to_email}
📎 PDF: Lebenslauf.pdf

-------------------------

{body}
""",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def confirm_sendbewerbung(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    to_email = context.user_data.get("pending_email")
    bewerbung_typ = context.user_data.get("bewerbung_typ", "it")
    subject = context.user_data.get("pending_subject")
    body = context.user_data.get("pending_body")

    if not to_email:
        await query.edit_message_text("❌ Keine Email zum Senden gefunden.")
        return

    try:
        send_email(
            to_email=to_email,
            subject=subject,
            body=body,
            attachment_path="Lebenslauf.pdf"
        )

        cursor.execute("""
        INSERT INTO applications (
            user_id,
            email,
            bewerbung_typ,
            sent_at
        )
        VALUES (?, ?, ?, ?)
        """, (
            update.effective_user.id,
            to_email,
            bewerbung_typ,
            datetime.now().strftime("%d.%m.%Y %H:%M")
        ))

        conn.commit()
        cursor.execute("""
        INSERT INTO companies (
            user_id,
            name,
            email,
            status
        )
        VALUES (?, ?, ?, ?)
        """, (
            update.effective_user.id,
            context.user_data.get("company_name"),
            to_email,
            "Bewerbung gesendet"
        ))

        conn.commit()

        context.user_data["pending_email"] = None
        context.user_data["bewerbung_typ"] = None
        context.user_data["pending_subject"] = None
        context.user_data["pending_body"] = None

        await query.edit_message_text(
            f"✅ Bewerbung wurde gesendet an:\n{to_email}\n\nTyp: {bewerbung_typ}"
        )

    except Exception as e:
        await query.edit_message_text(f"❌ Fehler beim Senden:\n{e}")


async def cancel_sendbewerbung(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data["pending_email"] = None
    context.user_data["bewerbung_typ"] = None
    context.user_data["pending_subject"] = None
    context.user_data["pending_body"] = None

    await query.edit_message_text("❌ Versand abgebrochen.")


async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cursor.execute("""
    SELECT email, bewerbung_typ, sent_at
    FROM applications
    WHERE user_id = ?
    ORDER BY id DESC
    """, (
        update.effective_user.id,
    ))

    applications = cursor.fetchall()

    if not applications:
        await update.message.reply_text("❌ Keine Bewerbungen gefunden.")
        return

    text = "📄 Deine Bewerbungen\n\n"

    for i, app in enumerate(applications, start=1):
        email = app[0]
        typ = app[1]
        date = app[2]

        text += (
            f"{i}. {typ} → {email}\n"
            f"📅 {date}\n\n"
        )

    await update.message.reply_text(text)


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    cursor.execute("""
    SELECT COUNT(*)
    FROM applications
    WHERE user_id = ?
    """, (user_id,))

    total = cursor.fetchone()[0]

    cursor.execute("""
    SELECT bewerbung_typ, COUNT(*)
    FROM applications
    WHERE user_id = ?
    GROUP BY bewerbung_typ
    """, (user_id,))

    rows = cursor.fetchall()

    text = f"📊 Statistik\n\nGesamt Bewerbungen: {total}\n\n"

    for typ, count in rows:
        text += f"{typ}: {count}\n"

    await update.message.reply_text(text)


async def clearhistory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    cursor.execute("""
    DELETE FROM applications
    WHERE user_id = ?
    """, (user_id,))

    conn.commit()

    await update.message.reply_text(
        "🧹 Bewerbungs-History gelöscht."
    )


async def export(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    cursor.execute("""
    SELECT email, bewerbung_typ, sent_at
    FROM applications
    WHERE user_id = ?
    ORDER BY id DESC
    """, (user_id,))

    rows = cursor.fetchall()

    if not rows:
        await update.message.reply_text(
            "❌ Keine Bewerbungen zum Exportieren."
        )
        return

    filename = "bewerbungen.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write("Bewerbungs-History\n\n")

        for i, row in enumerate(rows, start=1):
            email = row[0]
            typ = row[1]
            date = row[2]

            file.write(
                f"{i}. {typ}\n"
                f"Email: {email}\n"
                f"Datum: {date}\n\n"
            )

    await update.message.reply_document(
        document=open(filename, "rb")
    )