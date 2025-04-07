from flask_mailman import EmailMessage
from flask import current_app

def send_email(to, subject, body, from_email=None):
    if isinstance(to, str):
        to = [to]

    if from_email is None:
        from_email = current_app.config.get("MAIL_DEFAULT_SENDER")

    message = EmailMessage(
        subject=subject,
        body=body,
        from_email=from_email,
        to=to
    )

    message.send()