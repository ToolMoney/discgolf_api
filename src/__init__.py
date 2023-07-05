from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException


db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
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
    
    return json.dumps({
        "code": 500,
        "name": str(type(exception)),
        "description": str(exception),
    }), 500


from . import discs, courses, holes, rounds, scores
