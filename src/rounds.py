from . import app, db
from flask import request
from marshmallow import Schema, fields, EXCLUDE
from .scores import ScoreSchema
from flask_login import current_user, login_required


class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    date = db.Column(db.String)
    default_layout = db.Column(db.String)

    user = db.relationship("User")
    course = db.relationship("Course", back_populates="rounds")
    scores = db.relationship("Score", back_populates="round", cascade="all, delete-orphan")


class RoundSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    course_id = fields.Int(required=True)
    date = fields.Str()
    default_layout = fields.Str()
    scores = fields.List(fields.Nested(ScoreSchema))


@app.route("/rounds", methods=["GET"])
@login_required
def round_list():
    rounds = db.session.execute(
        db.select(Round)
        .where(Round.user_id == current_user.id)
        .order_by(Round.date.desc())
    ).scalars()
    return RoundSchema(many=True).dump(rounds)


@app.route("/rounds", methods=["POST"])
@login_required
def round_add():
    schema = RoundSchema()
    request_data = schema.load(request.json)
    new_round = Round(user_id=current_user.id, **request_data)
    db.session.add(new_round)
    db.session.commit()
    return schema.dump(new_round)


@app.route("/rounds/<int:id>", methods=["DELETE"])
@login_required
def round_delete(id):
    round = db.get_or_404(Round, id)
    db.session.delete(round)
    db.session.commit()
    return ({}, 204)


@app.route("/rounds/<int:id>", methods=["PUT"])
@login_required
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
@login_required
def round_details(id):
    round = db.session.execute(db.select(Round).where(Round.id == id)).scalar()
    return RoundSchema().dump(round)
