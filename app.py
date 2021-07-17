import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from flask_apscheduler import APScheduler
from flask_session import Session

load_dotenv(dotenv_path=str(Path(sys.argv[0]).parent / ".env"), verbose=True)

scheduler = APScheduler()


def create_app() -> Flask:
    """Create a new app instance."""
    app: Flask = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv("API_ID")
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = './session'

    Session(app)
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


if __name__ == '__main__':
    create_app().run()
