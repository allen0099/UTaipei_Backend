import typing as t
from http import HTTPStatus


class UTCAPIException(Exception):
    """Base exception for the application."""

    _http_code: int | HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR
    _default_message: str = "Unknown error."

    __slots__ = [
        "http_code",
        "detail_message",
        "parameters",
    ]

    def __init__(
        self,
        detail: str = "",
        *,
        http_code: int | str | HTTPStatus | None = None,
        **kwargs: t.Any,
    ):
        if http_code is None:
            http_code = self._http_code

        if detail == "":
            detail = self._default_message

        self.http_code = http_code
        self.detail_message = detail
        self.parameters = kwargs
