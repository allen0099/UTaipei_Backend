import typing as t
from http import HTTPStatus

from fastapi import Request
from starlette.responses import Response

from responses import error_response

from .. import UTCAPIException

__all__ = [
    "handle_all_exception",
    "handle_backend_api_exception",
]

_T = t.TypeVar("_T", UTCAPIException, Exception)


def handle_all_exception(_: Request, exc: Exception) -> Response:
    return error_response(
        {
            "detail": "Unknown error.",
            "parameters": exc.args,
        },
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
    )


def handle_backend_api_exception(_: Request, exc: _T) -> Response:
    return error_response(
        {
            "detail": exc.detail_message,
            "parameters": exc.parameters,
        },
        status_code=exc.http_code,
    )
