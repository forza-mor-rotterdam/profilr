import requests
from django.conf import settings
from django.core.cache import cache
from urllib.parse import urlencode
from apps.services.base import APIService


class ProfilrApi(APIService):
    _json_enabled = True

    def set_profile(self, user_token, data):
        return self.do_request("profile", user_token, method=APIService.POST, data=data, no_cache=True)

    def get_profile(self, user_token):
        return self.do_request("profile", user_token, no_cache=True)


profilr_api_service = ProfilrApi(f"{settings.PROFILR_API_URL}/v1")
