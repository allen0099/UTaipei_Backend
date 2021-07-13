from flask import jsonify, make_response

from api import api
from functions import get_semester, get_year


@api.route('/settings')
def settings():
    return make_response(jsonify({
        "year": get_year(),
        "semester": get_semester()
    }))
