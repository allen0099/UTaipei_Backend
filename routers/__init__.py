import logging

from fastapi import APIRouter, Response

from responses import success_response
from . import apis

logger: logging.Logger = logging.getLogger(__name__)

routes: APIRouter = APIRouter()

for route in [
    apis,
]:
    if hasattr(route, "router"):
        routes.include_router(route.router)


@routes.get("/healthcheck")
async def get_healthcheck() -> Response:
    """
    Health check
    """
    return success_response(data={"status": "ok"})
