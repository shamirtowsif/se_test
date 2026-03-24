from .settings import *


# Tests should run without depending on the Docker MySQL service.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test_db.sqlite3",
    }
}


PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]


MEDIA_ROOT = BASE_DIR / "test_media"
