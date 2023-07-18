from . import app, db
from flask import request
from marshmallow import Schema, fields, EXCLUDE
from flask_login import current_user


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    round_id = db.Column(db.Integer, db.ForeignKey('round.id'), nullable=False)
    hole_id = db.Column(db.Integer, db.ForeignKey('hole.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    user = db.relationship("User")
    round = db.relationship("Round", back_populates="scores")
    hole = db.relationship("Hole", back_populates="scores")


class ScoreSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    round_id = fields.Int(dump_only=True, required=True)
    hole_id = fields.Int(required=True)
    score = fields.Int(required=True)


@app.route("/rounds/<int:round_id>/scores", methods=["POST"])
def score_add(round_id):
    schema = ScoreSchema()
    request_data = schema.load(request.json)
    new_score = Score(user_id=current_user.id, **({"round_id": round_id} | request_data))
    db.session.add(new_score)
    db.session.commit()
    return schema.dump(new_score)


@app.route("/rounds/<int:round_id>/scores/<int:id>", methods=["DELETE"])
def score_delete(round_id, id):
    score = db.get_or_404(Score, id)
    db.session.delete(score)
    db.session.commit()
    return ({}, 204)


@app.route("/rounds/<int:round_id>/scores/<int:id>", methods=["PUT"])
def score_update(round_id, id):
    schema = ScoreSchema()
    updated_score = schema.load(request.json)
    score = db.get_or_404(Score, id)
    for key in updated_score:
        setattr(score, key, updated_score[key])

    db.session.add(score)
    db.session.commit()
    return schema.dump(score)
