from settings.settings import *

DEBUG = False

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(":")
CSRF_TRUSTED_ORIGINS = [os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS")]
