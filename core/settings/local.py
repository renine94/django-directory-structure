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

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        # 로컬 메모리 캐시 보는방법
        # from django.core.cache.backends import locmem
        # print(locmem._caches)
    },
    # "default": {
    #     "BACKEND": "django_redis.cache.RedisCache",
    #     "LOCATION": os.getenv('REDIS_HOST'),
    #     "OPTIONS": {
    #         "CLIENT_CLASS": "django_redis.client.DefaultClient",
    #     }
    # }
}

print(DATABASES)
print(CACHES)
