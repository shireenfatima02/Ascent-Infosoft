import smtplib
import ssl
from email.message import EmailMessage
from flask import current_app


def _parse_recipients(value) -> list[str]:
    if not value:
        return []
    if isinstance(value, (list, tuple, set)):
        recipients = [str(v).strip() for v in value if str(v).strip()]
        return recipients
    s = str(value)
    parts = []
    for chunk in s.replace(";", ",").split(","):
        chunk = chunk.strip()
        if chunk:
            parts.append(chunk)
    return parts


def send_email(message_body: str, subject: str = "Inquiry for Ascent Infosoft"):
    host = current_app.config.get("SMTP_HOST")
    port = current_app.config.get("SMTP_PORT")
    username = current_app.config.get("SMTP_USERNAME")
    password = current_app.config.get("SMTP_PASSWORD")
    use_ssl = current_app.config.get("SMTP_USE_SSL", True)
    recipients = _parse_recipients(current_app.config.get("SMTP_TO")) or ([username] if username else [])

    if not host or not username or not password:
        current_app.logger.warning("SMTP not configured; skipping email send.")
        return
    if not recipients:
        current_app.logger.warning("SMTP_TO not configured; skipping email send.")
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = username
    msg["To"] = ", ".join(recipients)
    msg.set_content(message_body)

    if use_ssl:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(username, password)
            # Provide explicit envelope recipients to avoid relying on header parsing.
            server.send_message(msg, from_addr=username, to_addrs=recipients)
    else:
        with smtplib.SMTP(host, port) as server:
            server.starttls(context=ssl.create_default_context())
            server.login(username, password)
            server.send_message(msg, from_addr=username, to_addrs=recipients)
