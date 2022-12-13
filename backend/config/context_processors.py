import requests
from django.conf import settings


def general_settings(context):
    PROFILR_API_AVAILABLE = False
    profilr_api_response = requests.get(settings.PROFILR_API_HEALTH_URL)
    if profilr_api_response and profilr_api_response.status_code == 200:
        PROFILR_API_AVAILABLE = True

    return {
        "git_sha": settings.GIT_SHA,
        "PROFILR_API_AVAILABLE": PROFILR_API_AVAILABLE,
        "ENABLE_MELDING_AFHANDELEN": settings.ENABLE_MELDING_AFHANDELEN,
        "ENABLE_AFDELING_RELATIES_ENDPOINT": settings.ENABLE_AFDELING_RELATIES_ENDPOINT,
    }
