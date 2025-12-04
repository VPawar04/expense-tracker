import smtplib
from email.message import EmailMessage
from config import Config


def send_email(to, subject, body):
    if not Config.MAIL_SERVER:
        return False

    msg = EmailMessage()
    msg['From'] = Config.MAIL_USERNAME
    msg['To'] = to
    msg['Subject'] = subject
    msg.set_content(body)

    with smtplib.SMTP(Config.MAIL_SERVER, int(Config.MAIL_PORT)) as smtp:
        smtp.starttls()
        smtp.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
        smtp.send_message(msg)

    return True
