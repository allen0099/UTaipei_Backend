from flask import Response, abort, redirect, request, session, url_for

from models import Classes, Timetable
from routes.api import api


@api.route("/search_time", methods=['POST'])
def search_time() -> Response:
    data: dict = request.form

    weekday: str = data['weekday']
    if weekday not in ['1', '2', '3', '4', '5', '6', '7']:
        return abort(404)

    class_time: str = data['time']
    if class_time not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']:
        return abort(404)

    _q = Classes.query \
        .filter(Classes.times.any(Timetable.weekday == __TimeMapper__[weekday])) \
        .filter(Classes.times.any(Timetable.time == class_time)) \
        .all()

    session["data"] = _q
    return redirect(url_for('routes.result'))


__TimeMapper__ = {
    '1': '一',
    '2': '二',
    '3': '三',
    '4': '四',
    '5': '五',
    '6': '六',
    '7': '日',
}
