import copy

from apps.services import msb_api_service, profilr_api_service
from apps.services.msb import DEFAULT_PROFILE
from django.conf import settings


class MSBUser:
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
                profile = profilr_api_service.get_profile(token)
            else:
                msb_api_service.get_user_info(token)
        except Exception:
            self._is_authenticated = False
        print("profile")
        print(profile)
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
            profile = profilr_api_service.set_profile(self.token, profile)

        self._profile = profile
        return self._profile

    @property
    def token(self):
        return self._request.session.get("token")

    @property
    def is_authenticated(self):
        return self._is_authenticated


class MSBAuthenticationBackend:
    def authenticate(self, request, username=None, password=None):
        success, token = msb_api_service.login(
            username,
            password,
        )
        print(success)
        print(token)
        request.session["token"] = token
        return (True, MSBUser(request)) if success else (False, token)


authenticate = MSBAuthenticationBackend().authenticate
