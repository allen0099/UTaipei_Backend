import inspect
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_apscheduler import APScheduler
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import BadRequest, Forbidden, InternalServerError, MethodNotAllowed, NotAcceptable, NotFound

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

        _error_page: str = "error.html"

        @app.errorhandler(400)
        def bad_request(error: BadRequest):
            return render_template(_error_page, error=error), 400

        @app.errorhandler(403)
        def forbidden(error: Forbidden):
            return render_template(_error_page, error=error), 403

        @app.errorhandler(404)
        def not_found(error: NotFound):
            return render_template(_error_page, error=error), 404

        @app.errorhandler(405)
        def method_not_allowed(error: MethodNotAllowed):
            return render_template(_error_page, error=error), 405

        @app.errorhandler(406)
        def not_acceptable(error: NotAcceptable):
            return render_template(_error_page, error=error), 406

        @app.errorhandler(500)
        def internal_server_error(error: InternalServerError):
            return render_template(_error_page, error=error), 500

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
