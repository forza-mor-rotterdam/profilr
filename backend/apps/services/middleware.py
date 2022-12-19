from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.utils.deprecation import MiddlewareMixin

from ..services.exceptions import (
    ApiServiceForbiddenException,
    ApiServiceNotFoundException,
)


class ApiServiceExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if issubclass(exception.__class__, ApiServiceNotFoundException):
            return HttpResponseNotFound()
        elif issubclass(exception.__class__, ApiServiceForbiddenException):
            return HttpResponseForbidden(status=401)
