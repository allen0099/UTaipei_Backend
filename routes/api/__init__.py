from flask import Blueprint

api: Blueprint = Blueprint("api", __name__, url_prefix="/api")

from .choose import choose
from .search_time import search_time
from .settings import settings
from .unit import get_unit
