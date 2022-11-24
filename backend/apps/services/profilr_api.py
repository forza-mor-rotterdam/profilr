import requests
from django.conf import settings
from django.core.cache import cache
from urllib.parse import urlencode
from apps.services.base import APIService


class ProfilrApi(APIService):
    url_base = f"{settings.PROFILR_API_URL}/v1"
    body_type = "json"
    default_headers = {}

    @classmethod
    def set_profile(cls, user_token, data):
        url = f"{cls.get_url_base()}/profile/"
        return cls.do_request(url, user_token, method=cls.POST, data=data, no_cache=True)

    @classmethod
    def get_profile(cls, user_token):
        url = f"{cls.get_url_base()}/profile/"
        return cls.do_request(url, user_token, no_cache=True)
