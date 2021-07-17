from flask import Blueprint, flash, redirect, render_template, session, url_for

from functions import get_semester, get_year

web_routes: Blueprint = Blueprint("routes", __name__)


@web_routes.route('/')
def search():
    return render_template('search.html')


@web_routes.route('/result')
def result():
    if session.get("data"):
        data: dict = session.get("data")
        if data.get("error"):
            flash(data.get("error"))
            return redirect(url_for('search'))
        total = data["total"]
        classes = data["classes"]
        return render_template('result.html', total=total, classes=classes, year=get_year(), semester=get_semester())
    return redirect(url_for('search'))


@web_routes.route('/my_table')
def my_table():
    return render_template('schedule.html', year=get_year(), semester=get_semester())
