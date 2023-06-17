from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

@app.after_request
def add_cors_header(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    return response


@app.route("/")
def hello_world():
    return "Hello world."

class Disc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    speed = db.Column(db.Integer)
    glide = db.Column(db.Integer)
    turn = db.Column(db.Integer)
    fade = db.Column(db.Integer)
    inBag = db.Column(db.Boolean)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "speed": self.speed,
            "glide": self.glide,
            "turn": self.turn,
            "fade": self.fade,
            "inBag": self.inBag,
            }
    

with app.app_context():
    db.create_all()

@app.route("/discs", methods=["GET"])
def disc_list():
    discs = db.session.execute(db.select(Disc).order_by(Disc.speed)).scalars()
    return [disc.to_dict() for disc in discs]


@app.route("/discs", methods=["POST"])
def disc_add():
    new_disc = Disc(**request.json)
    db.session.add(new_disc)
    db.session.commit()
    return new_disc.to_dict()

@app.route("/discs/<int:id>", methods=["DELETE"])
def disc_delete(id):
    disc = db.get_or_404(Disc, id)
    db.session.delete(disc)
    db.session.commit()
    return ({}, 204)

@app.route("/discs/<int:id>", methods=["PUT"])
def disc_update(id):
    updated_disc = request.json
    # TODO inBag case should be snake_case
    disc = db.get_or_404(Disc, id)
    for key in updated_disc:
        setattr(disc, key, updated_disc[key])

    db.session.add(disc)
    db.session.commit()
    return disc.to_dict()