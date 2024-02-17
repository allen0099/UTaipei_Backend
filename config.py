import logging
import logging.config
import os
from ast import literal_eval
from logging import Logger
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

logger: Logger = logging.getLogger(__name__)

_configs: dict[str, Any] = {
    "DEBUG": False,
    "RELOAD": False,
    "APP_NAME": "UTC Wrapper API",
}

# Define the base folder of the project
BASE_FOLDER: Path = Path(__file__).parent

# Define the logging config
LOGGING_LEVEL: int = logging.INFO
LOGGING_CONFIG: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "stdout": {
            "formatter": "console",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "stderr": {
            "formatter": "console",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "formatters": {
        "console": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "[%(levelname)s] %(asctime)s - %(name)s - %(message)s",
            "use_colors": True,
        },
        "file": {
            "()": "logging.Formatter",
            "fmt": "[%(levelname)s] %(asctime)s - %(name)s - %(message)s",
        },
        "access": {
            "()": "formatter.TimedAccessFormatter",
            "fmt": '[%(levelname)s] %(asctime)s %(client_addr)s - %(run_time)s "%(request_line)s" %(status_code)s %(response_length)s',
            "use_colors": True,
        },
        "access_file": {
            "()": "formatter.TimedAccessFormatter",
            "fmt": '[%(levelname)s] %(asctime)s %(client_addr)s - %(run_time)s "%(request_line)s" %(status_code)s %(response_length)s',
            "use_colors": False,
        },
    },
    "loggers": {
        "httpx": {"handlers": ["stderr"], "level": "INFO", "propagate": False},
        "access_time": {"handlers": ["access"], "level": "INFO", "propagate": False},
        "uvicorn": {"handlers": ["stderr"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"level": "INFO", "propagate": False},
    },
    "root": {"handlers": ["stderr"], "level": "INFO"},
}


def __load() -> None:
    """
    Load the environment variables from the .env file or os environment variables.

    Returns:
        None
    """
    env_file: Path = BASE_FOLDER / ".env"

    if os.path.isfile(env_file):
        logger.info("Loading environment variables from .env file.")
        load_dotenv(env_file)


def __convert_bool(value: str) -> bool:
    """
    Convert the string value to boolean value

    Args:
        value: The string value

    Returns:
        bool: The boolean value
    """
    if value.lower() in ["true", "t", "1", "yes", "y", "on"]:
        return True

    elif value.lower() in ["false", "f", "0", "no", "n", "off"]:
        return False

    else:
        raise ValueError(f"Cannot convert {value} to boolean value.")


def __auto_convert(env: Any) -> Any:
    """
    Auto convert the string value to the correct type.

    Args:
        env: The string value

    Returns:
        Any: The converted value
    """
    if isinstance(env, str):
        try:
            env = __convert_bool(env)

        except ValueError:
            try:
                # Auto guess type, only support int, float, list, dict
                env = literal_eval(env)

            except (ValueError, SyntaxError):
                pass
    elif env is None:
        env = None
    else:
        raise ValueError(f"Cannot convert {env}, should be a string.")

    return env


def __check_log_config() -> None:
    root_logger = logging.root
    root_logger.setLevel(LOGGING_LEVEL)

    # It means the logging config is not set, using the default config
    if len(root_logger.handlers) == 0:
        logging.config.dictConfig(LOGGING_CONFIG)

        logger.info("Using default logging config.")


def get(key: str, default: Any = None, *, convert: bool = False, raise_error: bool = False) -> Any:
    """
    Get the value of the key from the config file, if not found, return the default value

    Args:
        key: The key of the config
        default: The default value if the key is not found
        convert: If the value should be converted to the correct type, otherwise, return the string type value
        raise_error: If the key is not found and the default value is None, raise the KeyError

    Returns:
        Any: The value of the key
    """
    env: Any = os.getenv(key)

    if convert:
        env = __auto_convert(env)

    if env is not None:
        return env

    if key in _configs and _configs[key] is not None:
        return _configs[key]

    else:
        if raise_error and default is None:
            raise KeyError(f"Key {key} not found.")

        return default


__check_log_config()
__load()

DEBUG: bool = get("DEBUG", False, convert=True)
RELOAD: bool = get("RELOAD", False, convert=True)
