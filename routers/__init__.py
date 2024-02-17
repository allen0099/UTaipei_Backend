import logging

from fastapi import APIRouter

from . import apis

logger: logging.Logger = logging.getLogger(__name__)

routes: APIRouter = APIRouter(prefix="/api")

for route in [
    apis,
]:
    if hasattr(route, "router"):
        routes.include_router(route.router)
