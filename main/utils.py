from typing import Any, Optional

from django.core import mail
from django.core.mail import get_connection
from django.template import loader

from main.models import Setting


def get_email_backend():
    """
    Returns an email backend configured with the settings from the database.
    """
    if Setting.manager.read("email_backend") == "smtp":
        backend = "django.core.mail.backends.smtp.EmailBackend"  # pragma: no cover
    else:
        backend = "django.core.mail.backends.locmem.EmailBackend"

    return get_connection(
        backend=backend,
        host=Setting.manager.read("email_host", "localhost"),
        port=int(Setting.manager.read("email_port", "25")),
        username=Setting.manager.read("email_username", ""),
        password=Setting.manager.read("email_password", ""),
        use_tls=Setting.manager.read_boolean("email_use_tls", False),
        use_ssl=Setting.manager.read_boolean("email_use_ssl", False),
        fail_silently=False,
    )


def send_notification(
    subject: str,
    recipient_list: list[str],
    from_email: str,
    text_template: str,
    context: Optional[dict[str, Any]] = None,
    html_template: Optional[str] = None,
):
    email_backend = get_email_backend()

    plaintext_content = loader.render_to_string(text_template, context)

    html_content = None
    if html_template:
        html_content = loader.render_to_string(html_template, context)

    mail.send_mail(
        subject=subject,
        message=plaintext_content,
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=html_content,
        connection=email_backend,
    )
