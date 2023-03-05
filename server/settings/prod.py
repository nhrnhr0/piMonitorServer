from .base import *

DEBUG = False

ALLOWED_HOSTS = ['3.139.244.138','pi-monitor.boost-pop.com',]
CSRF_TRUSTED_ORIGINS = ['https://pi-monitor.boost-pop.com',]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


CHANNEL_LAYERS = {
        'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('localhost', 6379)],
        },
    },
}
