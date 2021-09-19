import secrets

from .settings_base import *


SECRET_KEY = secrets.token_urlsafe()
DEBUG = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "address_test",
        "USER": "testuser",
        "PASSWORD": "testuser",
        "HOST": "webapi-db",
        "PORT": "5432",
    }
}
