import logging

logger = logging.getLogger(__name__)


class ApiServiceBaseException(Exception):
    def __init__(self, *args, **kwargs):
        assert not args
        assert not kwargs


class ApiServiceException(ApiServiceBaseException):
    _default_message = None

    def __init__(self, message=None, *args, **kwargs):
        logger.error(f"default message: {self._default_message}, custom: {message}")
        super().__init__(*args, **kwargs)


class ApiServiceNotFoundException(ApiServiceException):
    _default_message = "API Service endpoint does not exists"


class ApiServiceForbiddenException(ApiServiceException):
    _default_message = "API Service endpoint forbidden"
