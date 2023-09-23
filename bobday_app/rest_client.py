import typing as t
from logging import getLogger
from json import dumps

import httpx

from .constants import DEFAULT_OK_CODES
from .exceptions import TimeoutException, NetworkError, HttpError, ApplicationError, exception_handler


class RestClient:

    def __init__(self, url: str, auth: tuple[str, str], headers: dict = {}):
        self.url = url
        self.headers = headers
        self.logger = getLogger("RestClient")
        self.auth = httpx.BasicAuth(*auth)

    @exception_handler((TimeoutException, NetworkError, HttpError), ApplicationError)
    def __call__(self, method, data: dict = {}) -> dict[str, t.Any]:
        response = httpx.request(
            method,
            self.url,
            headers=self.headers,
            data=dumps(data),
            auth=self.auth
        )

        if response.status_code not in DEFAULT_OK_CODES:
            raise HttpError(response.status_code)

        return response.json()
