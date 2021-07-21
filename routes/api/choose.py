from flask import Response, abort, redirect, request, session, url_for

from functions import get_semester, get_values, get_year
from models import Classes, Teachers
from routes.api import api


@api.route("/choose", methods=['POST'])
def choose() -> Response:
    data: dict = request.form

    options = get_values(get_year(), get_semester())
    degree: str = data.get('degree')
    if degree not in options["degree"]:
        return abort(404)

    department: str = data.get("department")
    if department not in options["department"]:
        return abort(404)

    unit: str = data.get("unit")
    if unit not in options["unit"]:
        return abort(404)

    class_year: str = data.get("year")
    if class_year not in options["class_year"]:
        return abort(404)

    class_type: str = data.get("type")
    if class_type not in [_[0] for _ in options["crk"]]:
        return abort(404)

    course_name: str = data.get("subject")
    teacher: str = data.get("teacher")

    Classes.query.filter_by()

    _q = Classes.query

    if degree != "%":
        _q = _q.filter_by(_degree=degree)
    if department != "%":
        _q = _q.filter_by(_department=department)
    if unit != "%":
        _q = _q.filter_by(_unit=unit)
    if class_year != "%":
        _q = _q.filter_by(_class_year=class_year)
    if class_type != "%":
        _q = _q.filter_by(_class_type=class_type)

    if course_name != "" or course_name is not None:
        _q = _q.filter(Classes.chinese_name.like(f"%{course_name}%"))

    if teacher != "" or teacher is not None:
        _q = _q.join(Classes.teachers).filter(Teachers.name.like(f"%{teacher}%"))

    _q = _q.all()
    session["data"] = _q
    return redirect(url_for('routes.result'))
