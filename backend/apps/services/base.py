import requests
from requests import Response
from django.conf import settings
from django.core.cache import cache
from urllib.parse import urlencode


class BaseAPIService:

    def __init__(self, *args, **kwargs):
        assert not args
        assert not kwargs

    def get_headers(self):
        if type(self.default_headers) is not dict:
            raise NotImplementedError
        return self.default_headers


class APIService(BaseAPIService):
    _api_base_url: str = None
    _headers: dict = {}
    _json_enabled: bool = False
    _timeout = (5, 10)
    _cache_timeout = 60 * 5

    GET = "get"
    POST = "post"

    def __init__(self, api_base_url: str, *args, **kwargs):
        self._api_base_url = api_base_url.strip().rstrip("/")
        super().__init__(*args, **kwargs)

    def add_headers(self, headers: dict) -> dict:
        self._headers = self._headers.update(headers)
        return self._headers

    def remove_headers(self, header_key: str) -> dict:
        self._headers.pop(header_key)
        return self._headers

    @classmethod
    def get_user_token_from_request(cls, request) -> tuple[str, None]:
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        auth_parts = auth_header.split(" ") if auth_header else []
        if len(auth_parts) == 2 and auth_parts[0] == "Bearer":
            return auth_parts[1]
        return

    def process_response(self, response: Response) -> Response:
        return response

    def do_request(
        self,
        path,
        user_token=None,
        method=GET,
        data={},
        no_cache=False,
        cache_timeout=_cache_timeout,
        raw_response=False,
    ) -> tuple[Response, dict, list]:
        url = f"{self._api_base_url}/{path}"
        cache_key = f"{url}?{urlencode(data)}"
        response = cache.get(cache_key)
        action = getattr(requests, method, APIService.GET)
        if not response or no_cache:
            headers = self._headers
            if user_token:
                headers.update({"Authorization": f"Bearer {user_token}"})
            action_params = {
                "url": url,
                "headers": headers,
                "json" if self._json_enabled else "data" : data,
                "timeout": self._timeout,
            }
            response = action(**action_params)
            response.raise_for_status()

            if int(response.status_code) >= 200 and int(response.status_code) < 300:
                cache.set(cache_key, response, cache_timeout)
        else:
            print(f"fetch from cache: {url}")
        return response if raw_response else self.process_response(response)
