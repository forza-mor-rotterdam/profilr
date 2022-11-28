import requests
from django.conf import settings
from django.core.cache import cache
from urllib.parse import urlencode
from apps.services.base import APIService
from requests import Response


class MSBService(APIService):
    def process_response(self, response: Response) -> tuple[list, dict]:
        response = response.json()
        return response.get("result")

    def logout(self):
        return self.do_request(
            "logout", no_cache=True
        )

    def login(self, username: str, password: str):
        data = {
            "uid": username,
            "pwd": password,
        }
        response_data = self.do_request(
            "login", user_token=None, method=APIService.POST, data=data, no_cache=True
        )
        response_data = response_data.json()
        return bool(response_data.get("success")), response_data.get("result")

    def get_user_info(self, user_token):
        return self.do_request("gebruikerinfo", user_token, no_cache=True)

    def get_list(self, user_token, data={}, no_cache=False):
        return self.do_request("msb/openmeldingen", user_token, APIService.POST, data, no_cache)

    def get_detail(self, melding_id, user_token):
        return self.do_request(f"msb/melding/{melding_id}", user_token, cache_timeout=30)

    def get_mutatieregels(self, melding_id, user_token):
        return self.do_request(f"msb/melding/{melding_id}/mutatieregels", user_token, cache_timeout=30)
    
    def get_foto(self, foto_id, user_token, thumbnail=False):
        data = {}
        if thumbnail:
            data.update({"thumbnail": thumbnail})
        return self.do_request(f"msb/melding/foto/{foto_id}", user_token, data=data, raw_response=True)

    def get_wijken(self, user_token):
        return self.do_request("wijken", user_token)

    def get_onderwerpgroepen(self, user_token):
        return self.do_request("msb/onderwerpgroepen", user_token)

    def get_afdelingen(self, user_token):
        return self.do_request("msb/afdelingen", user_token)

msb_api_service = MSBService(f"{settings.MSB_API_URL}/sbmob/api")
