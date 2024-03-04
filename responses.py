import logging
import math
import typing as t
from datetime import datetime
from http import HTTPStatus

from starlette.background import BackgroundTask
from starlette.responses import JSONResponse
from starlette.responses import Response

logger: logging.Logger = logging.getLogger(__name__)


class SuccessResponse(JSONResponse):
    key: str = "data"

    def __init__(
        self,
        data: t.Any = None,
        *,
        status_code: int | HTTPStatus = HTTPStatus.OK,
        headers: t.Optional[t.Mapping[str, str]] = None,
        media_type: t.Optional[str] = None,
        background: t.Optional[BackgroundTask] = None,
    ) -> None:
        super().__init__(
            self.generate_content(data),
            status_code,
            headers,
            media_type,
            background,
        )

    def generate_content(self, data: t.Any) -> dict[str, t.Any]:
        if data is None:
            data = ""

        return {
            self.key: data,
            "datetime": datetime.now().isoformat(),
        }


class ErrorResponse(SuccessResponse):
    key: str = "error"


def success_response(
    data: t.Any = None,
    *,
    status_code: int | HTTPStatus = HTTPStatus.OK,
    headers: t.Optional[t.Mapping[str, str]] = None,
    media_type: t.Optional[str] = None,
    background: t.Optional[BackgroundTask] = None,
) -> Response:
    if math.floor(status_code / 100) in (4, 5):
        raise ValueError("4xx and 5xx are not success response.")

    if data is None:
        data = "success"

    return SuccessResponse(
        data,
        status_code=status_code,
        headers=headers,
        media_type=media_type,
        background=background,
    )


def error_response(
    data: t.Any = None,
    *,
    status_code: int | HTTPStatus = HTTPStatus.BAD_REQUEST,
    headers: t.Optional[t.Mapping[str, str]] = None,
    media_type: t.Optional[str] = None,
    background: t.Optional[BackgroundTask] = None,
) -> Response:
    if math.floor(status_code / 100) not in (4, 5):
        raise ValueError("4xx and 5xx are not error response.")

    if not data:
        data = "error"

    return ErrorResponse(
        data,
        status_code=status_code,
        headers=headers,
        media_type=media_type,
        background=background,
    )
