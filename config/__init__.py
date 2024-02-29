import logging.config
from logging import Logger

from .common import BASE_FOLDER, DEBUG, RELOAD, get
from .logger import LOGGING_CONFIG

logger: Logger = logging.getLogger(__name__)
