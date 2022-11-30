import os
from os.path import join

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRUE_VALUES = [True, "True", "true", "1"]

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", os.environ.get("APP_SECRET"))

ENVIRONMENT = os.getenv("ENVIRONMENT")
DEBUG = ENVIRONMENT == "development"

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

USE_TZ = True
TIME_ZONE = "Europe/Amsterdam"
USE_L10N = True
LANGUAGE_CODE = "nl-NL"

DEFAULT_ALLOWED_HOSTS = ".forzamor.nl,localhost,127.0.0.1"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", DEFAULT_ALLOWED_HOSTS).split(",")

GIT_SHA = os.environ.get("GITHUB_SHA", "no_git_sha")

FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://profilr.forzamor.nl")
PROJECT_URL = os.environ.get("PROJECT_URL", FRONTEND_URL)
ENABLE_PROFILR_API = os.environ.get("ENABLE_PROFILR_API", True) in TRUE_VALUES

INSTALLED_APPS = (
    "django.contrib.staticfiles",
    "django.contrib.sessions",
    "rest_framework",
    "webpack_loader",
    "health_check",
    "health_check.cache",
    "health_check.storage",
    # Apps
    "apps.profilr",
    "apps.health",
)

MIDDLEWARE = (
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

STATIC_URL = "/static/"
STATIC_ROOT = os.path.normpath(join(os.path.dirname(BASE_DIR), "static"))

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.normpath(join(os.path.dirname(BASE_DIR), "media"))

WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": not DEBUG,
        "POLL_INTERVAL": 0.1,
        "IGNORE": [r".+\.hot-update.js", r".+\.map"],
        "LOADER_CLASS": "config.webpack.ExternalWebpackLoader",
        "STATS_URL": f"{FRONTEND_URL}/build/webpack-stats.json",
    }
}

CORS_ORIGIN_WHITELIST = ()
CORS_ORIGIN_ALLOW_ALL = False

USE_X_FORWARDED_HOST = True

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "config.context_processors.general_settings",
            ],
        },
    }
]

# SECURE_SSL_REDIRECT = not DEBUG
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

REDIS_URL = "redis://redis:6379"
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
        },
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

MSB_API_URL = os.getenv("MSB_API_URL", "https://diensten.rotterdam.nl")
PROFILR_API_URL = os.getenv("PROFILR_API_URL", "https://api.profilr.forzamor.nl")
