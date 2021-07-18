import inspect
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from flask_apscheduler import APScheduler
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

load_dotenv(dotenv_path=str(Path(sys.argv[0]).parent / ".env"), verbose=True)

db: SQLAlchemy = SQLAlchemy()
scheduler: APScheduler = APScheduler()


def create_app() -> Flask:
    """Create a new app instance."""
    app: Flask = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv("API_ID")
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = './session'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    Session(app)
    db.init_app(app)
    scheduler.init_app(app)

    with app.app_context():
        import schedule
        print(schedule)
        scheduler.start()

        # register blueprints
        from routes.api import api
        app.register_blueprint(api)
        from routes import web_routes
        app.register_blueprint(web_routes)

        return app


app: Flask = create_app()


# For flask shell debug use
@app.shell_context_processor
def make_shell_context() -> dict:
    import models
    return dict(
        db=db,
        **dict(
            inspect.getmembers(models, inspect.isclass)
        )
    )


if __name__ == '__main__':
    app.run()
