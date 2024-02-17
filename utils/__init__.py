import logging
from datetime import date

logger: logging.Logger = logging.getLogger(__name__)


def get_semester() -> int:
    today: date = date.today()
    return 1 if today.month > 5 else 2


def get_year() -> int:
    today: date = date.today()
    return today.year - 1911 if today.month > 5 else today.year - 1912
