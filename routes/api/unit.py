from flask import jsonify, make_response, request

from functions import get_units
from routes.api import api


@api.route('get_unit')
def get_unit():
    dept: str = request.args.get('dept', default="%", type=str)
    return make_response(jsonify(get_units(dept)))
