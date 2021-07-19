from flask import Response, make_response, request, session

from routes.api import api


@api.route("/remove_query", methods=['POST'])
def remove_query() -> Response:
    data: dict = request.form

    class_id: str = data['id']

    if session.get("query"):
        session.get("query").remove(class_id)

    return make_response('', 204)
