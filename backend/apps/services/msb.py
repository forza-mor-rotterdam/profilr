import copy

from apps.services.base import APIService
from django.conf import settings
from requests import Response

DEFAULT_FILTERS = {
    "wijken": [],
    "buurten": [],
    "afdelingen": [],
    "groepen": [],
    "onderwerpen": [],
}
DEFAULT_PROFILE = {"filters": DEFAULT_FILTERS}
VALID_FILTERS = ("wijken", "buurten", "afdelingen", "groepen", "onderwerpen")


class MSBService(APIService):
    def validate_filters(self, filters: dict) -> dict:
        filters = copy.deepcopy(filters)
        {
            k: v if type(v) == list else [v] if type(v) in [str, int, float] else []
            for k, v in filters.items()
            if k in VALID_FILTERS
        }
        for k in VALID_FILTERS:
            if not filters.get(k):
                filters[k] = []
        return filters

    def process_response(self, response: Response) -> tuple[list, dict]:
        response = response.json()
        return response.get("result")

    def logout(self):
        return self.do_request("logout", no_cache=True)

    def login(self, username: str, password: str):
        data = {
            "uid": username,
            "pwd": password,
        }
        response_data = self.do_request(
            "login",
            user_token=None,
            method=APIService.POST,
            data=data,
            no_cache=True,
            raw_response=True,
        )
        response_data = response_data.json()
        return bool(response_data.get("success")), response_data.get("result")

    def get_user_info(self, user_token):
        return self.do_request("gebruikerinfo", user_token, no_cache=True)

    def get_list(self, user_token, data={}, no_cache=False):
        return self.do_request(
            "msb/openmeldingen", user_token, APIService.POST, data, no_cache
        )

    def get_detail(self, melding_id, user_token):
        return self.do_request(
            f"msb/melding/{melding_id}", user_token, cache_timeout=30
        )

    def get_mutatieregels(self, melding_id, user_token):
        return self.do_request(
            f"msb/melding/{melding_id}/mutatieregels", user_token, cache_timeout=30
        )

    def get_foto(self, foto_id, user_token, thumbnail=False):
        data = {}
        if thumbnail:
            data.update({"thumbnail": thumbnail})
        return self.do_request(
            f"msb/melding/foto/{foto_id}",
            user_token,
            data=data,
            raw_response=True,
            cache_timeout=60 * 60,
        )

    def get_wijken(self, user_token):
        return self.do_request("wijken", user_token)

    def get_onderwerpgroepen(self, user_token):
        return self.do_request("msb/onderwerpgroepen", user_token)

    def get_afdelingen(self, user_token):
        return self.do_request("msb/afdelingen", user_token)

    def afhandelen(self, melding_id: str, user_token: str, data: dict):
        """
        {
            "meldingId":2407629,
            "behandelaar":"Behandelaar naam",
            "meldingType":"O",
            "afhandelOpmerking":"De gemeente is aan de slag gegaan met uw melding en volgens onze gegevens is het probleem opgelost. Daarom sluiten we uw melding.",
            "straat":"55832",
            "huisnummer":"205",
            "plaatsbepaling":null,
            "x":92396,
            "y":437830
        }

        {
            "meldingId":2407694,
            "behandelaar":"Behandelaar naam",
            "meldingType":"N",
            "redenAfhandelenNiet":"73",
            "afhandelOpmerking":"De (brom)fiets is volgens onze richtlijnen geen wrak. Daarom verwijderen we deze niet. Kijk op https://www.rotterdam.nl/wonen-leven/handhaving/ voor meer informatie. We sluiten uw melding.",
            "straat":"82821",
            "huisnummer":"54",
            "plaatsbepaling":"Alternatieve plaatsbepaling",
            "x":92355,
            "y":437451,
            "fotos":[{}]
        }
        """
        if settings.ENABLE_MELDING_AFHANDELEN:
            return self.do_request(
                f"msb/melding/{melding_id}/afhandelen",
                user_token,
                data=data,
                method=APIService.POST,
                no_cache=True,
            )
        return self.get_detail(melding_id, user_token)


msb_api_service = MSBService(f"{settings.MSB_API_URL}/sbmob/api")
