import os

import dj_database_url
import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

root = environ.Path(__file__, "../..")

os.sys.path.insert(0, root())
os.sys.path.insert(0, os.path.join(root(), "apps"))

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ["*"]),
    SECRET_KEY=(str, "=ees8976541f=g0_bzup_0a(m^4@4+ke395t3fruaoj!z#lleivq"),
    LANGUAGE_CODE=(str, "en"),
    DB_USER=(str, "user"),
    DB_PASS=(str, "pass"),
    DB_HOST=(str, "pg"),
    DB_NAME=(str, "main"),
    BASE_URL=(str, "http://localhost:8000"),
    ROLE=(str, "prod"),
    REDIS_DSN=(str, "redis://redis:6379/0"),
    SENTRY_DSN=(str, None),
)

SENTRY_DSN = env("SENTRY_DSN")
RAVEN_CONFIG = {"dsn": SENTRY_DSN}
if SENTRY_DSN:
    sentry_sdk.init(dsn=SENTRY_DSN, integrations=[DjangoIntegration()])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROLE = env("ROLE")

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")
CORS_ORIGIN_ALLOW_ALL = True

INSTALLED_APPS = [
    "solo",
    "modeltranslation",
    "django.contrib.sitemaps",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "adminsortable2",
    "corsheaders",
    "django_dramatiq",
    "django_json_widget",
    "martor",
    "rest_framework",
    "apps.api.apps.ApiConfig",
    "apps.common.apps.CommonConfig",
    "apps.requirement.apps.RequirementConfig",
]
if SENTRY_DSN:
    INSTALLED_APPS += ["raven.contrib.django.raven_compat"]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
if SENTRY_DSN:
    MIDDLEWARE += ["raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware"]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [root("project/templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "project.wsgi.application"

DB_USER = env("DB_USER")
DB_PASS = env("DB_PASS")
DB_HOST = env("DB_HOST")
DB_NAME = env("DB_NAME")
DATABASES = {"default": dj_database_url.config(default=f"postgres://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")}
FIXTURE_DIRS = [root("project/fixtures")]

REDIS_DSN = env("REDIS_DSN")

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

USE_TZ = True
TIME_ZONE = "UTC"

LANGUAGE_CODE = env("LANGUAGE_CODE")
gettext = lambda s: s
LANGUAGES = (
    ("ru", gettext("Russian")),
    ("en", gettext("English")),
)
USE_I18N = True
USE_L10N = True

MODELTRANSLATION_LANGUAGES = ("en", "ru")

MEDIA_URL = "/media/"
MEDIA_ROOT = root("media")

STATIC_URL = "/static/"
STATIC_ROOT = root("static")
STATICFILES_DIRS = [root("project/static")]

BASE_URL = env("BASE_URL")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

MARTOR_UPLOAD_URL = "/admin/martor/uploader/"
MARTOR_MARKDOWNIFY_URL = "/admin/martor/markdownify/"
MARTOR_SEARCH_USERS_URL = "/admin/martor/search-user/"

REST_FRAMEWORK_EXTENSIONS = {"DEFAULT_CACHE_RESPONSE_TIMEOUT": 1}
REST_FRAMEWORK = {
    "PAGE_SIZE": 100,
    "UPLOADED_FILES_USE_URL": env("ROLE") != "test",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

DRAMATIQ_TASKS_DATABASE = "default"
DRAMATIQ_RESULT_BACKEND = {
    "BACKEND": "dramatiq.results.backends.redis.RedisBackend",
    "BACKEND_OPTIONS": {"url": "redis://localhost:6379"},
    "MIDDLEWARE_OPTIONS": {"result_ttl": 60000},
    "heartbeat_interval": 13,
}
DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.redis.RedisBroker",
    "OPTIONS": {"url": REDIS_DSN},
    "MIDDLEWARE": [
        "dramatiq.middleware.AgeLimit",
        "dramatiq.middleware.TimeLimit",
        "dramatiq.middleware.Callbacks",
        "dramatiq.middleware.Retries",
    ],
}

# DRAMATIQ_BROKER = {
#     "BROKER": "dramatiq.brokers.stub.StubBroker",
#     "OPTIONS": {},
#     "MIDDLEWARE": [
#         "dramatiq.middleware.AgeLimit",
#         "dramatiq.middleware.TimeLimit",
#         "dramatiq.middleware.Callbacks",
#         "dramatiq.middleware.Pipelines",
#         "dramatiq.middleware.Retries",
#         "django_dramatiq.middleware.DbConnectionsMiddleware",
#         "django_dramatiq.middleware.AdminMiddleware",
#     ]
# }

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "root": {"level": "WARNING", "handlers": ["console"]},
    "formatters": {"verbose": {"format": "%(levelname)s  %(asctime)s  %(module)s: %(message)s"}},
    "handlers": {"console": {"level": "DEBUG", "class": "logging.StreamHandler", "formatter": "verbose"}},
    "loggers": {
        "django.server": {"level": "DEBUG", "handlers": ["console"], "propagate": False},
        "django.request": {"level": "INFO", "handlers": ["console"], "propagate": False},
        "django.db.backends": {"level": "ERROR", "handlers": ["console"], "propagate": False},
    },
}
if SENTRY_DSN:
    LOGGING["root"]["handlers"] += "sentry"

    LOGGING["handlers"]["sentry"] = {
        "level": "ERROR",
        "class": "raven.contrib.django.raven_compat.handlers.SentryHandler",
    }

    LOGGING["loggers"]["raven"] = {"level": "DEBUG", "handlers": ["console"], "propagate": False}
    LOGGING["loggers"]["sentry.errors"] = {"level": "DEBUG", "handlers": ["console"], "propagate": False}

if ROLE == "test":

    class DisableMigrations:
        def __contains__(self, item):
            return True

        def __getitem__(self, item):
            return None

    MIGRATION_MODULES = DisableMigrations()
