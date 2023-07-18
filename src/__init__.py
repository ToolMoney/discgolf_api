from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import traceback

db = SQLAlchemy()
app = Flask(__name__, instance_relative_config=True)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
app.config.from_file("config.json", load=json.load)
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = True
bcrypt = Bcrypt(app)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response.headers["Access-Control-Allow-Headers"] = "content-type"
    response.headers["Access-Control-Allow-Methods"] = "GET, PUT, DELETE, POST"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


@app.errorhandler(HTTPException)
def handle_http_exception(exception):
    response = exception.get_response()
    response.data = json.dumps({
        "code": exception.code,
        "name": exception.name,
        "description": exception.description,
    })
    response.content_type = "application/json"
    return response


@app.errorhandler(Exception)
def handle_exception(exception):
    if isinstance(exception, HTTPException):
        return exception

    app.logger.error('An error occurred: %s', exception)
    print(traceback.format_exc())
    return json.dumps({
        "code": 500,
        "name": str(type(exception)),
        "description": str(exception),
    }), 500


from . import discs, courses, holes, rounds, scores, users
