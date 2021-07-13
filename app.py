import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, session, url_for
from flask_session import Session

from api import api
from api.settings import get_semester, get_year

load_dotenv(dotenv_path=str(Path(sys.argv[0]).parent / ".env"), verbose=True)

app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config['SECRET_KEY'] = os.getenv("API_ID")
app.config['SESSION_FILE_DIR'] = './session'
app.config.from_object(__name__)
Session(app)
app.register_blueprint(api)


@app.route('/')
def search():
    return render_template('search.html')


@app.route('/result')
def result():
    # TODO: add warning sign at the last col in result table
    if session.get("data"):
        data: dict = session.get("data")
        if data.get("error"):
            flash(data.get("error"))
            return redirect(url_for('search'))
        total = data["total"]
        classes = data["classes"]
        return render_template('result.html', total=total, classes=classes)
    return redirect(url_for('search'))


@app.route('/my_table')
def hello_world():
    return render_template('schedule.html', year=get_year(), semester=get_semester())


if __name__ == '__main__':
    app.run()
