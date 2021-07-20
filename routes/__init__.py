from flask import Blueprint, redirect, render_template, session, url_for

from functions import get_semester, get_year
from models import Classes, Timetable

web_routes: Blueprint = Blueprint("routes", __name__)


@web_routes.route('/')
def search():
    return render_template('search.html')


@web_routes.route('/result')
def result():
    if session.get("data"):
        data: list[Classes] = session.get("data")
        total = len(data)
        return render_template('result.html', total=total, classes=data, year=get_year(), semester=get_semester())
    return redirect(url_for('routes.search'))


@web_routes.route('/query_result')
def query_result():
    return render_template('query_result.html', year=get_year(), semester=get_semester())


@web_routes.route('/my_table')
def my_table():
    times: list[Timetable] = []
    classes: list[Classes] = []

    if session.get("query"):
        for _ in session.get("query"):
            _q: list[Timetable] = Timetable.query.filter_by(class_id=_).all()
            for t in _q:
                times.append(t)
            _c: Classes = Classes.query.filter_by(id=_).first()
            classes.append(_c)

    __mapper__: dict = {
        "一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "日": 7,
    }
    # https://stackoverflow.com/a/17109098
    times.sort(key=lambda x: (int(x.time), __mapper__[x.weekday]))

    return render_template('schedule.html', times=times, classes=classes,
                           year=get_year(), semester=get_semester(), d_map=__mapper__,
                           d_time=list(dict.fromkeys([_.time for _ in times])))
