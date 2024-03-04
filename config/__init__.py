import logging.config
from logging import Logger

from .common import BASE_FOLDER
from .common import DEBUG
from .common import RELOAD
from .common import get
from .logger import LOGGING_CONFIG

logger: Logger = logging.getLogger(__name__)
