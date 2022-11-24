import requests
from django.conf import settings
from django.core.cache import cache
from urllib.parse import urlencode
from apps.services.base import APIService


class MSBService(APIService):
    url_base = f"{settings.MSB_API_URL}/sbmob/api"
    default_headers = {}
    body_type = "data"
    default_timeout = (5, 10)
    default_cache_timeout = 60 * 5
    GET = "get"
    POST = "post"

    @classmethod
    def do_blob_request(
        cls,
        url,
        user_token,
        data={},
        no_cache=False,
        cache_timeout=default_cache_timeout,
    ):
        response = cache.get(f"{url}?{urlencode(data)}")
        if not response or no_cache:
            headers = {}
            if user_token:
                headers.update({"Authorization": f"Bearer {user_token}"})
            response = requests.get(
                url=url,
                params=data,
                headers=headers,
                timeout=cls.default_timeout,
            )
            cache.set(f"{url}?{urlencode(data)}", response, cache_timeout)
        else:
            print(f"fetch from cache: {url}")
        return response

    @classmethod
    def logout(cls):
        url = f"{cls.get_url_base()}/logout"
        return cls.do_request(
            url, no_cache=True
        )

    @classmethod
    def login(cls, username: str, password: str):
        url = f"{cls.get_url_base()}/login"
        data = {
            "uid": username,
            "pwd": password,
        }
        response_data = cls.do_request(
            url, user_token=None, method=cls.POST, data=data, no_cache=True
        )
        return bool(response_data.get("success")), response_data.get("result")

    @classmethod
    def get_user_info(cls,user_token):
        url = f"{cls.get_url_base()}/gebruikerinfo"
        return cls.do_request(url, user_token, no_cache=True)

    @classmethod
    def get_list(cls, user_token, data={}, no_cache=False):
        url = f"{cls.get_url_base()}/msb/openmeldingen"
        return cls.do_request(url, user_token, MSBService.POST, data, no_cache)

    @classmethod
    def get_detail(cls,melding_id, user_token):
        url = f"{cls.get_url_base()}/msb/melding/{melding_id}"
        return cls.do_request(url, user_token, cache_timeout=30)

    @classmethod
    def get_mutatieregels(cls,melding_id, user_token):
        url = f"{cls.get_url_base()}/msb/melding/{melding_id}/mutatieregels"
        return cls.do_request(url, user_token, cache_timeout=30)
    
    @classmethod
    def get_foto(cls,foto_id, user_token, thumbnail=False):
        url = f"{cls.get_url_base()}/msb/melding/foto/{foto_id}"
        data = {}
        if thumbnail:
            data.update({"thumbnail": thumbnail})
        return cls.do_blob_request(url, user_token, data=data)

    @classmethod
    def get_wijken(cls,user_token):
        url = f"{cls.get_url_base()}/wijken"
        return cls.do_request(url, user_token)

    @classmethod
    def get_onderwerpgroepen(cls,user_token):
        url = f"{cls.get_url_base()}/msb/onderwerpgroepen"
        response = cls.do_request(url, user_token)
        return response

    @classmethod
    def get_afdelingen(cls,user_token):
        url = f"{cls.get_url_base()}/msb/afdelingen"
        return cls.do_request(url, user_token)
