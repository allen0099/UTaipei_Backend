import logging.config
import os
from logging import Logger
from pathlib import Path
from typing import Any

from .common import DEBUG, BASE_FOLDER

logger: Logger = logging.getLogger(__name__)

LOG_FOLDER: Path = BASE_FOLDER / "logs"

if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

LOGFILES: dict[str, Path] = {
    "console": LOG_FOLDER / "console.log",
    "access": LOG_FOLDER / "access.log",
    "sql": LOG_FOLDER / "sql.log",
}

FORMATS: dict[str, str] = {
    "console": "[%(levelname)s] %(asctime)s - %(name)s - %(message)s",
    "access": '[%(levelname)s] %(asctime)s %(client_addr)s - %(run_time)s "%(request_line)s" %(status_code)s %(response_length)s',
}
FORMATTERS: dict[str, dict[str, str]] = {
    "console": {
        "()": "uvicorn.logging.DefaultFormatter",
        "fmt": FORMATS["console"],
        "use_colors": True,
    },
    "console_log": {
        "()": "logging.Formatter",
        "fmt": FORMATS["console"],
    },
    "access": {
        "()": "formatter.TimedAccessFormatter",
        "fmt": FORMATS["access"],
        "use_colors": True,
    },
    "access_log": {
        "()": "formatter.TimedAccessFormatter",
        "fmt": FORMATS["access"],
        "use_colors": False,
    },
}

HANDLER: dict[str, str] = {
    "stream": "logging.StreamHandler",
    "file": "logging.handlers.TimedRotatingFileHandler",
}
HANDLERS: dict[str, dict[str, str]] = {
    "stdout": {
        "formatter": "console",
        "class": HANDLER["stream"],
        "stream": "ext://sys.stdout",
    },
    "stderr": {
        "formatter": "console",
        "class": HANDLER["stream"],
        "stream": "ext://sys.stderr",
    },
    "access": {
        "formatter": "access",
        "class": HANDLER["stream"],
        "stream": "ext://sys.stdout",
    },
    "consolelog": {
        "formatter": "console_log",
        "class": HANDLER["file"],
        "filename": LOGFILES["console"],
        "when": "D",
        "delay": True,
        "backupCount": 30,
        "encoding": "utf8",
    },
    "accesslog": {
        "formatter": "access_log",
        "class": HANDLER["file"],
        "filename": LOGFILES["access"],
        "when": "D",
        "delay": True,
        "backupCount": 5,
        "encoding": "utf8",
    },
    "sqllog": {
        "formatter": "console_log",
        "class": HANDLER["file"],
        "filename": LOGFILES["sql"],
        "when": "D",
        "delay": True,
        "backupCount": 5,
        "encoding": "utf8",
    },
}

LOGGING_CONFIG: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": HANDLERS,
    "formatters": FORMATTERS,
    "loggers": {
        "httpx": {"level": "INFO"},
        "httpcore": {"level": "INFO"},
        "http_client": {"level": "INFO"},
        "access_time": {"handlers": ["access", "consolelog", "accesslog"], "level": "INFO", "propagate": False},
        "sqlalchemy": {"handlers": ["sqllog"], "level": "INFO", "propagate": False},
        # "sqlalchemy.engine": {"level": "WARN"},
        "sqlalchemy.orm": {"propagate": False},
        "uvicorn": {"handlers": ["stderr", "consolelog"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"level": "INFO", "propagate": False},
    },
    "root": {"handlers": ["stdout", "consolelog"], "level": "DEBUG" if DEBUG else "INFO"},
}

root_logger = logging.root

if len(root_logger.handlers) == 0:
    logging.config.dictConfig(LOGGING_CONFIG)

    # For logfiles, input new line to indicate the start of the log
    for logfile in LOGFILES.values():
        with open(logfile, "a") as f:
            f.write("====== NEW APPLICATION START ======\n")

    logger.info("Using default logging config.")
