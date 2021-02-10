import logging
from typing import Any

import requests
from django.conf import settings

__all__ = ["get_object_or_none", "sent_via_send_grid"]

logger = logging.getLogger("django.request")


def get_object_or_none(model: Any, *args, **kwargs) -> Any:
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def sent_via_send_grid(email: str, template_id: str, context: dict = None) -> None:
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {settings.SENDGRID_TOKEN}"}
    data = {
        "from": {"email": settings.EMAIL_FROM},
        "template_id": template_id,
        "personalizations": [{"to": [{"email": email}], "dynamic_template_data": context or {}}],
    }

    log_msg = f"Set email to {email} template_id={template_id}"
    try:
        res: requests.Response = requests.post("https://api.sendgrid.com/v3/mail/send", json=data, headers=headers)

        if res.status_code == 400:
            msg = f"Bad SendGrid message format {log_msg}:\n{res.json()}"
            logger.error(msg)
            raise Exception(msg)

        elif res.status_code == 401:
            msg = f"Send Grid API Key is wrong {log_msg}"
            logger.error(msg)

            raise Exception(msg)

        elif res.status_code == 202:
            logger.info(f"Email was sent {log_msg}")

        elif res.status_code == 429:
            msg = f"SendGrid Rate Limits {log_msg}"
            logger.error(msg)

            raise Exception(msg)

        elif res.status_code >= 500:
            msg = f"Error occurred on SendGrid side. Status code is {res.status_code}. {log_msg}"
            logger.exception(msg)

            raise Exception(msg)

    except Exception as e:
        logger.exception(f"Error occurred at sending email via SendGrid {log_msg}")

        raise e
