# Builtins
from typing import List
import os

# 3rd party
from requests import Response, post


class MailGun:
    MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")

    FROM_TITLE = "stores rest api"
    FROM_EMAIL = "postmaster@sandbox63f52a2fd65c43e1be80407d95199d3e.mailgun.org"

    @classmethod
    def send_email(
        cls, email: List[str], subject: str, text: str, html: str
    ) -> Response:
        return post(
            f"http://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth=("api", cls.MAILGUN_API_KEY),
            data={
                "from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                "to": email,
                "subject": subject,
                "text": text,
                "html": html,
            },
        )

