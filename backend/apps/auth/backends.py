import copy

from apps.services import incident_api_service, profile_api_service
from django.conf import settings
from profilr_api_services import MSB_DEFAULT_FILTERS

DEFAULT_PROFILE = {"filters": MSB_DEFAULT_FILTERS}


class IncidentUser:
    _is_authenticated = None
    _token = None
    _profile = None
    _request = None
    _name = None
    _email = None

    def __init__(self, request, *args, **kwargs):
        self._request = request
        token = request.session.get("token")
        self._is_authenticated = True
        profile = request.session.get("profile", copy.deepcopy(DEFAULT_PROFILE))
        try:
            if settings.ENABLE_PROFILR_API:
                profile = profile_api_service.get_profile(token)
            else:
                incident_api_service.get_user_info(token)
        except Exception:
            self._is_authenticated = False

        self._name = profile.get("user", {}).get("name", "No name")
        if token:
            self._profile = profile

    @property
    def profile(self):
        return self._profile

    @property
    def name(self):
        return self._name

    def set_profile(self, profile):
        self._request.session["profile"] = profile
        if settings.ENABLE_PROFILR_API:
            profile = profile_api_service.set_profile(self.token, profile)

        self._profile = profile
        return self._profile

    @property
    def token(self):
        return self._request.session.get("token")

    @property
    def is_authenticated(self):
        return self._is_authenticated


class IncidentAuthenticationBackend:
    def authenticate(self, request, username=None, password=None):
        success, token = incident_api_service.login(
            username,
            password,
        )
        request.session["token"] = token
        return (True, IncidentUser(request)) if success else (False, token)


authenticate = IncidentAuthenticationBackend().authenticate
