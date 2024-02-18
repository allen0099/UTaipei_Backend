import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

import config
import routers
from exceptions import UTCAPIException
from exceptions.handlers import handle_all_exception, handle_backend_api_exception
from middlewares import LogRequestMiddleware

logger: logging.Logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    middleware: list[Middleware] = [
        Middleware(
            CORSMiddleware,  # type: ignore
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
            allow_credentials=True,
        ),
        Middleware(LogRequestMiddleware),  # type: ignore
    ]

    if config.DEBUG:
        app: FastAPI = FastAPI(
            debug=True,
            title=config.get("APP_NAME"),
            middleware=middleware,
        )

    else:
        app: FastAPI = FastAPI(
            title=config.get("APP_NAME"),
            middleware=middleware,
            openapi_url="",
            docs_url="",
            redoc_url="",
        )

    app.add_exception_handler(Exception, handle_all_exception)
    app.add_exception_handler(UTCAPIException, handle_backend_api_exception)
    app.include_router(routers.routes)

    return app


if __name__ == "__main__":
    if config.DEBUG:
        uvicorn.run(
            "main:create_app",
            host=config.get("HOST"),
            port=int(config.get("PORT")),
            reload=config.RELOAD,
            factory=True,
            log_config=config.LOGGING_CONFIG,
        )

    else:
        uvicorn.run(
            "main:create_app",
            host="0.0.0.0",
            port=8080,
            factory=True,
            log_config=config.LOGGING_CONFIG,
        )
