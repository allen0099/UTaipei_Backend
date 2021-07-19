from flask import jsonify, make_response

from models import Config
from routes.api import api


@api.route('update_time')
def update_time():
    c: Config = Config.query.filter_by(key="UPDATE_TIME").first()

    if not c:
        return make_response(jsonify({
            "error": "database not exist!"
        }))

    return make_response(jsonify({
        "time": c.value
    }))
