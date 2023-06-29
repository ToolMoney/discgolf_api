from . import app, db
from flask import request
from marshmallow import Schema, fields, EXCLUDE
from .scores import ScoreSchema


class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    # user = db.Column()
    default_layout = db.Column(db.String)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    scores = db.relationship("Score", back_populates="round")
    course = db.relationship("Course", back_populates="rounds")
    

class RoundSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    date = fields.Str()
    default_layout = fields.Str()
    course_id = fields.Int(required=True)
    scores = fields.List(fields.Nested(ScoreSchema))


with app.app_context():
    db.create_all()


@app.route("/rounds", methods=["GET"])
def round_list():
    rounds = db.session.execute(db.select(Round).order_by(Round.date.desc())).scalars()
    return RoundSchema(many=True).dump(rounds)

@app.route("/rounds", methods=["POST"])
def round_add():
    schema = RoundSchema()
    request_data = schema.load(request.json)
    new_round = Round(**request_data)
    db.session.add(new_round)
    db.session.commit()
    return schema.dump(new_round)

@app.route("/rounds/<int:id>", methods=["DELETE"])
def round_delete(id):
    round = db.get_or_404(Round, id)
    db.session.delete(round)
    db.session.commit()
    return ({}, 204)

@app.route("/rounds/<int:id>", methods=["PUT"])
def round_update(id):
    schema = RoundSchema()
    updated_round = schema.load(request.json)
    round = db.get_or_404(Round, id)
    for key in updated_round:
        setattr(round, key, updated_round[key])

    db.session.add(round)
    db.session.commit()
    return schema.dump(round)


@app.route("/rounds/<int:id>", methods=["GET"])
def round_details(id):
    round = db.session.execute(db.select(Round).where(Round.id == id)).scalar()
    return RoundSchema().dump(round)