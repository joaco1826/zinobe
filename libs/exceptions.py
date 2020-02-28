from http import HTTPStatus


class ZinobeException(Exception):
    """Base class for other exceptions"""
    def __init__(self, message, status_code):
        super(ZinobeException, self).__init__(message)
        self.status_code = status_code


class TokenNotFound(ZinobeException):
    """Raised when there is no token in the request"""
    def __init__(self):
        super(TokenNotFound, self).__init__(
            "Token not found!", HTTPStatus.BAD_REQUEST
        )


class ExternalRequestFailed(ZinobeException):
    """Raised when a request to an external service fails"""
    def __init__(self):
        super(ExternalRequestFailed, self).__init__(
            "External request failed!", HTTPStatus.INTERNAL_SERVER_ERROR
        )
