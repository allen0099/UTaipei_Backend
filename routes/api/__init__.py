from flask import Blueprint

api: Blueprint = Blueprint("api", __name__, url_prefix="/api")

from .add_query import add_query
from .choose import choose
from .remove_query import remove_query
from .search_time import search_time
from .settings import settings
from .unit import get_unit
from .update_time import update_time
