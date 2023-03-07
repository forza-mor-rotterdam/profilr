import requests
from django.conf import settings


def general_settings(request):
    PROFILE_API_AVAILABLE = False
    profile_api_response = None
    try:
        profile_api_response = requests.get(settings.PROFILE_API_HEALTH_CHECK_URL)
    except Exception:
        pass
    if profile_api_response and profile_api_response.status_code == 200:
        PROFILE_API_AVAILABLE = True

    # request.user.profile
    profile = request.user.profile if hasattr(request, "user") else None

    return {
        "git_sha": settings.GIT_SHA,
        "PROFILE_API_AVAILABLE": PROFILE_API_AVAILABLE,
        "ENABLE_MELDING_AFHANDELEN": settings.ENABLE_MELDING_AFHANDELEN,
        "ENABLE_AFDELING_RELATIES_ENDPOINT": settings.ENABLE_AFDELING_RELATIES_ENDPOINT,
        "PROFILE_API_URL": settings.PROFILE_API_URL,
        "INCIDENT_API_URL": settings.INCIDENT_API_URL,
        "FRONTEND_URL": settings.FRONTEND_URL,
        "PROJECT_URL": settings.PROJECT_URL,
        "UI_SETTINGS": settings.UI_SETTINGS,
        "profile": profile,
    }
