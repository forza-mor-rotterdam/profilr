import locale
import os
import sys
from os.path import join

locale.setlocale(locale.LC_ALL, "nl_NL.UTF-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRUE_VALUES = [True, "True", "true", "1"]

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY", os.getenv("SECRET_KEY", os.getenv("APP_SECRET"))
)

ENVIRONMENT = os.getenv("ENVIRONMENT")
DEBUG = ENVIRONMENT == "development"

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

USE_TZ = True
TIME_ZONE = "Europe/Amsterdam"
USE_L10N = True
USE_I18N = True
LANGUAGE_CODE = "nl-NL"
LANGUAGES = [("nl", "Dutch")]

DEFAULT_ALLOWED_HOSTS = ".forzamor.nl,localhost,127.0.0.1"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", DEFAULT_ALLOWED_HOSTS).split(",")

GIT_SHA = os.getenv("GITHUB_SHA", "no_git_sha")

FRONTEND_URL = os.getenv("FRONTEND_URL", "https://profilr.forzamor.nl")
PROJECT_URL = os.getenv("PROJECT_URL", FRONTEND_URL)


MSB_API_URL = os.getenv("MSB_API_URL")
INCIDENT_API_URL = os.getenv("INCIDENT_API_URL", f"{MSB_API_URL}/sbmob/api")
INCIDENT_API_HEALTH_CHECK_URL = os.getenv(
    "INCIDENT_API_HEALTH_CHECK_URL", f"{MSB_API_URL}/health"
)
INCIDENT_API_SERVICE = os.getenv(
    "INCIDENT_API_SERVICE", "profilr_api_services.IncidentAPIService"
)

PROFILR_API_URL = os.getenv("PROFILR_API_URL")
PROFILE_API_URL = os.getenv("PROFILE_API_URL", f"{PROFILR_API_URL}/v1")
PROFILE_API_HEALTH_CHECK_URL = os.getenv(
    "PROFILE_API_HEALTH_CHECK_URL", f"{PROFILR_API_URL}/health/"
)
PROFILE_API_SERVICE_EXCEPTION_MIDDLEWARE = os.getenv(
    "PROFILE_API_SERVICE_EXCEPTION_MIDDLEWARE",
    "profilr_api_services.middleware.ApiServiceExceptionMiddleware",
)
PROFILE_API_SERVICE = os.getenv(
    "PROFILE_API_SERVICE", "profilr_api_services.ProfileAPIService"
)

ENABLE_PROFILR_API = os.getenv("ENABLE_PROFILR_API", True) in TRUE_VALUES

ENABLE_MELDING_AFHANDELEN = os.getenv("ENABLE_MELDING_AFHANDELEN", False) in TRUE_VALUES
ENABLE_AFDELING_RELATIES_ENDPOINT = (
    os.getenv("ENABLE_AFDELING_RELATIES_ENDPOINT", True) in TRUE_VALUES
)
MSB_ENABLE_AFDELING_RELATIES_ENDPOINT = ENABLE_AFDELING_RELATIES_ENDPOINT
MSB_ENABLE_MELDING_AFHANDELEN = ENABLE_MELDING_AFHANDELEN

UI_SETTINGS = {"fontsizes": ["fz-medium", "fz-large", "fz-xlarge"]}

INSTALLED_APPS = (
    "django.contrib.staticfiles",
    "django.contrib.sessions",
    "rest_framework",
    "webpack_loader",
    "corsheaders",
    "health_check",
    "health_check.cache",
    "health_check.storage",
    # Apps
    "apps.profilr",
    "apps.health",
    "apps.auth",
)

LOGIN_URL = "/login/"

MIDDLEWARE = (
    "profilr_api_services.middleware.ApiServiceExceptionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django_permissions_policy.PermissionsPolicyMiddleware",
    "csp.middleware.CSPMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "apps.auth.middleware.AuthenticationMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

# django-permissions-policy settings
PERMISSIONS_POLICY = {
    "accelerometer": [],
    "ambient-light-sensor": [],
    "autoplay": [],
    "camera": [],
    "display-capture": [],
    "document-domain": [],
    "encrypted-media": [],
    "fullscreen": [],
    "geolocation": [],
    "gyroscope": [],
    "interest-cohort": [],
    "magnetometer": [],
    "microphone": [],
    "midi": [],
    "payment": [],
    "usb": [],
}

AUTHENTICATION_BACKENDS = ["apps.auth.backends.MSBAuthenticationBackend"]

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

# Django security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_REFERRER_POLICY = "strict-origin"
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "SAMEORIGIN"
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD = True
CORS_ORIGIN_WHITELIST = ()
CORS_ORIGIN_ALLOW_ALL = False
USE_X_FORWARDED_HOST = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_NAME = "__Secure-sessionid" if not DEBUG else "sessionid"
CSRF_COOKIE_NAME = "__Secure-csrftoken" if not DEBUG else "csrftoken"
SESSION_COOKIE_SAMESITE = "Strict" if not DEBUG else "Lax"
CSRF_COOKIE_SAMESITE = "Strict" if not DEBUG else "Lax"

# Settings for Content-Security-Policy header
CSP_DEFAULT_SRC = ("'self'",) if not DEBUG else ("'self'", PROJECT_URL)
CSP_FRAME_ANCESTORS = ("'self'",)
CSP_SCRIPT_SRC = (
    ("'self'", "'unsafe-eval'", "unpkg.com")
    if not DEBUG
    else ("'self'", "'unsafe-eval'", "unpkg.com", PROJECT_URL)
)
CSP_IMG_SRC = (
    ("'self'", "data:", "unpkg.com", "tile.openstreetmap.org")
    if not DEBUG
    else ("'self'", "data:", "unpkg.com", "tile.openstreetmap.org", PROJECT_URL)
)
CSP_STYLE_SRC = (
    ("'self'", "'unsafe-inline'", "unpkg.com")
    if not DEBUG
    else ("'self'", "'unsafe-inline'", "unpkg.com", PROJECT_URL)
)
CSP_CONNECT_SRC = ("'self'",) if not DEBUG else ("'self'", "ws:")

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

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
