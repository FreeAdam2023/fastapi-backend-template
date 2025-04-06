"""
@Time ： 2025-04-05
@Auth ： Adam Lyu
"""

# app/services/email/client.py

from email.message import EmailMessage
import aiosmtplib
from app.core.config import settings


class MailClient:
    def __init__(self):
        self.hostname = settings.MAIL_SERVER
        self.port = settings.MAIL_PORT
        self.username = settings.MAIL_USERNAME
        self.password = settings.MAIL_PASSWORD
        self.start_tls = settings.MAIL_USE_TLS
        self.use_tls = settings.MAIL_USE_SSL
        self.default_sender = settings.MAIL_DEFAULT_SENDER

    async def send(self, to: str, subject: str, content: str, html: str = None):
        msg = EmailMessage()
        msg["From"] = self.default_sender
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(content)
        if html:
            msg.add_alternative(html, subtype="html")

        await aiosmtplib.send(
            msg,
            hostname=self.hostname,
            port=self.port,
            username=self.username,
            password=self.password,
            start_tls=self.start_tls,
            use_tls=self.use_tls,
        )


mailer = MailClient()
