import requests
from django.conf import settings
from health_check.backends import BaseHealthCheckBackend
from health_check.exceptions import HealthCheckException


class ProfileAPIHealthCheck(BaseHealthCheckBackend):
    critical_service = False

    def check_status(self):
        health_check_response = requests.get(settings.PROFILE_API_HEALTH_CHECK_URL)

        if health_check_response.status_code != 200:
            raise HealthCheckException(
                f"Profile API not ready: status code: {health_check_response.status_code}"
            )
        if health_check_response.status_code == 404:
            raise HealthCheckException(
                f"Profile API: health url not implemented: status code: {health_check_response.status_code}"
            )

    def identifier(self):
        return self.__class__.__name__


class IncidentAPIHealthCheck(BaseHealthCheckBackend):
    critical_service = True

    def check_status(self):
        health_check_response = requests.get(settings.INCIDENT_API_HEALTH_CHECK_URL)

        if health_check_response.status_code != 200:
            raise HealthCheckException(
                f"Incident API not ready: status code: {health_check_response.status_code}"
            )

    def identifier(self):
        return self.__class__.__name__
