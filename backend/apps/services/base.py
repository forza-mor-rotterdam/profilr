import requests
from django.conf import settings
from django.core.cache import cache
from urllib.parse import urlencode


class APIService:
    # url_base = f"{settings.MSB_API_URL}/sbmob/api"
    default_timeout = (5, 10)
    default_cache_timeout = 60 * 5
    GET = "get"
    POST = "post"

    @classmethod
    def get_url_base(cls):
        if not cls.url_base:
            raise NotImplementedError
        return cls.url_base

    @classmethod
    def get_headers(cls):
        if type(cls.default_headers) is not dict:
            raise NotImplementedError
        return cls.default_headers

    @classmethod
    def get_body_type(cls):
        if not cls.body_type:
            raise NotImplementedError
        return cls.body_type

    @classmethod
    def get_user_token_from_request(cls, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        auth_parts = auth_header.split(" ") if auth_header else []
        if settings.MSB_USER_TOKEN:
            return settings.MSB_USER_TOKEN
        if len(auth_parts) == 2 and auth_parts[0] == "Bearer":
            return auth_parts[1]

    @classmethod
    def do_request(
        cls,
        url,
        user_token=None,
        method=GET,
        data={},
        no_cache=False,
        cache_timeout=default_cache_timeout,
    ):
        json_response = cache.get(url)
        action = getattr(requests, method, "get")
        if not json_response or no_cache:
            headers = cls.get_headers()
            if user_token:
                headers.update({"Authorization": f"Bearer {user_token}"})
            action_params = {
                "url": url,
                "headers": headers,
                cls.get_body_type(): data,
                "timeout": cls.default_timeout,
            }
            response = action(**action_params)

            json_response = response.json()
            cache.set(url, json_response, cache_timeout)
        else:
            print(f"fetch from cache: {url}")
        return json_response
