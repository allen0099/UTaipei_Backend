from flask import Blueprint, redirect, render_template, session, url_for

from functions import get_semester, get_year
from models import Classes

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
    return render_template('query_result.html')


@web_routes.route('/my_table')
def my_table():
    return render_template('schedule.html', year=get_year(), semester=get_semester())
