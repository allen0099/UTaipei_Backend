from flask import Response, make_response, request, session

from models import Classes
from routes.api import api


@api.route("/add_query", methods=['POST'])
def add_query() -> Response:
    data: dict = request.form

    class_id: str = data['id']

    _q: Classes = Classes.query.filter_by(id=class_id).first_or_404()

    if session.get("query"):
        session.get("query").append(_q.id)

    else:
        session["query"] = [_q.id]

    return make_response('', 204)
