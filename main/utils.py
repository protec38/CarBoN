from django.core.mail import get_connection

from main.models import Setting

def get_email_backend():
    """
    Returns an email backend configured with the settings from the database.
    """
    if Setting.manager.read("email_backend") == "smtp":
        backend = "django.core.mail.backends.smtp.EmailBackend"
    else:
        backend = "django.core.mail.backends.locmem.EmailBackend"


    return get_connection(backend=backend,
        host=Setting.manager.read("email_host", "localhost"),
        port=int(Setting.manager.read("email_port", "25")),
        username=Setting.manager.read("email_username", ""),
        password=Setting.manager.read("email_password", ""),
        use_tls=Setting.manager.read_boolean("email_use_tls", False),
        use_ssl=Setting.manager.read_boolean("email_use_ssl", False),
        fail_silently=False,
    )
