from .base import *


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql_psycopg2",
#         "NAME": os.getenv('DB_NAME'),
#         "USER": os.getenv('DB_USER'),
#         "PASSWORD": os.getenv('DB_PASSWORD'),
#         "HOST": os.getenv('DB_HOST'),
#         "PORT": os.getenv('DB_PORT'),
#         'ATOMIC_REQUESTS': True,
#     },
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

