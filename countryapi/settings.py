import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
import dj_database_url


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))


SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",


    "rest_framework",

 
    "countries",  
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "countryapi.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "countryapi.wsgi.application"

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=False
    )
}


AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = os.environ.get("TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  
STATICFILES_DIRS = [BASE_DIR / "static"]  


STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    # "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    # "PAGE_SIZE": int(os.environ.get("DRF_PAGE_SIZE", 50)),
    'EXCEPTION_HANDLER': 'countries.exceptions.custom_exception_handler',
}

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "%(levelname)s %(asctime)s %(name)s %(message)s"},
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": str(LOG_DIR / "app.log"),
            "formatter": "verbose",
        },
    },
    "root": {"handlers": ["console", "file"], "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO")},
    "loggers": {
       
        "django.db.backends": {"level": "WARNING", "handlers": ["console"], "propagate": False},
    },
}


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "default-cache",
    }
}


CACHE_DIR = BASE_DIR / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",") if os.environ.get("CSRF_TRUSTED_ORIGINS") else []

if not DEBUG:

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 25) or 25)
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "False").lower() in ("1", "true", "yes")

if DEBUG:
    print(">>> Running with DEBUG=True. Make sure to set DJANGO_DEBUG=False in production and configure SECRET_KEY, DATABASE_URL, and ALLOWED_HOSTS.")

