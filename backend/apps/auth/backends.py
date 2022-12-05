# from django.contrib.auth.backends import RemoteUserBackend
from apps.services import msb_api_service, profilr_api_service


class MSBUser:
    _token = None
    _profile = None

    def __init__(self, token, *args, **kwargs):
        profile = profilr_api_service.get_profile(token)
        if token:
            self._token = token
            self._profile = profile

    @property
    def profile(self):
        return self._profile

    def set_profile(self, profile):
        profile = profilr_api_service.set_profile(self._token, profile)
        self._profile = profile
        return self._profile

    @property
    def token(self):
        return self._token

    @property
    def is_authenticated(self):
        return self._token

    def logout(self):
        self._token = None


class MSBAuthenticationBackend:
    def authenticate(self, request, username=None, password=None):
        success, token = msb_api_service.login(
            username,
            password,
        )
        request.session["token"] = token
        return MSBUser(token) if success else None


authenticate = MSBAuthenticationBackend().authenticate
