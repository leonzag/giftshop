import os
from pathlib import Path

from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", get_random_secret_key)
DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "true"
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "shop.apps.ShopConfig",
    "cart.apps.CartConfig",
    "orders.apps.OrdersConfig",
    "coupons.apps.CouponsConfig",
    "account.apps.AccountConfig",
    "info.apps.InfoConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "myshop.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "shop.context_processors.categories",
                "cart.context_processors.cart",
            ],
            "libraries": {
                "filters": "filters.filters",
            },
        },
    },
]

WSGI_APPLICATION = "myshop.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST", "db"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_ROOT = BASE_DIR / "static/"
STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Media files (user-uploaded files)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media/"

# Session settings
CART_SESSION_ID = "cart"
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL", "redis://redis:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
ADMIN_EMAIL_ADDRESS = "admin@myshop.com"
CONTACT_EMAIL_ADDRESS = "leonzag@yandex.ru"

# Celery
rmq_user = os.environ.get("RABBITMQ_USER")
rmq_pwd = os.environ.get("RABBITMQ_PASSWORD")

CELERY_BROKER_URL = f"amqp://{rmq_user}:{rmq_pwd}@rabbitmq:5672/"  # URL брокера сообщений (RabbitMQ)
CELERY_RESULT_BACKEND = "redis://redis:6379/0"  # Где Celery будет хранить результаты задач. /0 - это номер БД Redis
CELERY_ACCEPT_CONTENT = ["json"]  # Какие типы контента Celery должен принимать
CELERY_TASK_SERIALIZER = "json"  # Как задачи будут сериализоваться
CELERY_RESULT_SERIALIZER = "json"  # Как результаты будут сериализоваться
CELERY_TIMEZONE = "Europe/Moscow"

CELERY_TASK_ALWAYS_EAGER = False  # Важно для продакшена (True - для тестирования задач синхронно)
CELERY_TASK_EAGER_PROPAGATES_EXCEPTIONS = False  # Аналогично

# Account
LOGIN_REDIRECT_URL = "/"  # Переход на главную страницу после успешного входа
LOGIN_URL = "/account/login/"  # Куда перенаправляется пользователь для входа
LOGOUT_REDIRECT_URL = "/"  # Переход пользователя после выхода
