import copy

from apps.services import msb_api_service, profilr_api_service
from apps.services.msb import DEFAULT_PROFILE
from django.conf import settings


class MSBUser:
    _token = None
    _profile = None
    _request = None

    def __init__(self, request, *args, **kwargs):
        self._request = request
        token = request.session.get("token")
        profile = request.session.get("profile", copy.deepcopy(DEFAULT_PROFILE))
        try:
            if settings.ENABLE_PROFILR_API:
                profile = profilr_api_service.get_profile(token)
            else:
                msb_api_service.get_user_info(token)
        except Exception:
            request.session.flush()

        if token:
            self._profile = profile

    @property
    def profile(self):
        return self._profile

    def set_profile(self, profile):
        self._request.session["profile"] = profile
        try:
            if settings.ENABLE_PROFILR_API:
                profile = profilr_api_service.set_profile(self.token, profile)
        except Exception:
            self._request.session.flush()

        self._profile = profile
        return self._profile

    @property
    def token(self):
        return self._request.session.get("token")

    @property
    def is_authenticated(self):
        return self._request.session.get("token")


class MSBAuthenticationBackend:
    def authenticate(self, request, username=None, password=None):
        success, token = msb_api_service.login(
            username,
            password,
        )
        request.session["token"] = token
        return MSBUser(request) if success else None


authenticate = MSBAuthenticationBackend().authenticate
