# Builtins
from typing import List
from enum import Enum
import os

# 3rd party
from requests import Response, post


class MailGunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class ExceptionTypes(Enum):
    API_KEY = "Failed to load MailGun API Key"
    DOMAIN = "Failed to load MailGun domain"
    CONFIRMATION_FAILURE = "Confirmation email failure, registration failed"


class MailGun:
    MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")

    FROM_TITLE = "stores rest api"
    FROM_EMAIL = "postmaster@sandbox63f52a2fd65c43e1be80407d95199d3e.mailgun.org"

    @classmethod
    def send_email(
        cls, email: List[str], subject: str, text: str, html: str
    ) -> Response:
        # not evaluates falsey values
        # is None only works for None
        # if environ.get can't find value it will set field to None
        if cls.MAILGUN_API_KEY is None:
            raise MailGunException(ExceptionTypes.API_KEY)
        if cls.MAILGUN_DOMAIN is None:
            raise MailGunException(ExceptionTypes.DOMAIN)

        response = post(
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

        if response.status_code != 200:
            raise MailGunException(ExceptionTypes.CONFIRMATION_FAILURE)
        return response

