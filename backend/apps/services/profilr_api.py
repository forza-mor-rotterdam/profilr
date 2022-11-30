from apps.services.base import APIService
from django.conf import settings


class ProfilrApi(APIService):
    _json_enabled = True

    def set_profile(self, user_token, data):
        return self.do_request(
            "profile/", user_token, method=APIService.POST, data=data, no_cache=True
        ).json()

    def get_profile(self, user_token):
        return self.do_request("profile/", user_token, no_cache=True).json()


profilr_api_service = ProfilrApi(f"{settings.PROFILR_API_URL}/v1")
