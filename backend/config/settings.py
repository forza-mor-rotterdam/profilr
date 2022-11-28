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

DEFAULT_ALLOWED_HOSTS = ".forzamor.nl,localhost,127.0.0.1"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", DEFAULT_ALLOWED_HOSTS).split(",")

FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://profilr.forzamor.nl")

INSTALLED_APPS = (
    "django.contrib.staticfiles",
    "django.contrib.sessions",
    "rest_framework",
    "webpack_loader",
    # Apps
    "apps.profilr",
)

MIDDLEWARE = (
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
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
        # 'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
        "POLL_INTERVAL": 0.1,
        "IGNORE": [r".+\.hot-update.js", r".+\.map"],
        "LOADER_CLASS": "config.webpack.ExternalWebpackLoader",
        # Custom config setting made available in WebpackLoader's self.config
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
            ],
        },
    }
]

# SECURE_SSL_REDIRECT = DEBUG
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SESSION_COOKIE_SECURE = not DEBUG
# CSRF_COOKIE_SECURE = not DEBUG

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/var/tmp/django_cache",
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

MSB_API_URL = os.getenv("MSB_API_URL", "https://diensten.rotterdam.nl")
PROFILR_API_URL = os.getenv("PROFILR_API_URL", "https://api.profilr.forzamor.nl")
