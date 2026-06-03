import smtplib
import os

from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(to_email, subject, body, attachments=None):
    msg = EmailMessage()

    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.set_content(body)

    if attachments:
        for attachment_path in attachments:
            if not os.path.exists(attachment_path):
                raise FileNotFoundError(
                    f"Datei nicht gefunden: {attachment_path}"
                )

            with open(attachment_path, "rb") as file:
                file_data = file.read()
                file_name = os.path.basename(attachment_path)

            msg.add_attachment(
                file_data,
                maintype="application",
                subtype="pdf",
                filename=file_name
            )

    with smtplib.SMTP_SSL("mail.gmx.net", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

    print("✅ Email gesendet")