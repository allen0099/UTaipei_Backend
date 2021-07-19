from flask import Response, jsonify, make_response, session

from models import Classes
from routes.api import api


@api.route("/query")
def get_query() -> Response:
    return_data: list[dict] = []

    query_list: list[str] = session.get("query")
    if query_list:
        for cls_id in query_list:
            _cls: Classes = Classes.query.filter_by(id=cls_id).first()
            return_data.append(_cls.serialize())

    return make_response(jsonify(return_data))
