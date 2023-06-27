from . import app, db
from flask import request


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    round_id = db.Column(db.Integer, db.ForeignKey('round.id'))
    hole_id = db.Column(db.Integer, db.ForeignKey('hole.id'))
    score = db.Column(db.Integer)
    
    round = db.relationship("Round", back_populates="scores")
    hole = db.relationship("Hole", back_populates="scores")

    def to_dict(self):
        return {
            "id": self.id,
            "round_id": self.round_id,
            "hole_id": self.hole_id,
            "score": self.score,
        }



with app.app_context():
    db.create_all()


@app.route("/rounds/<int:round_id>/scores", methods=["POST"])
def score_add(round_id):
    new_score = Score(**({"round_id": round_id} | request.json))
    db.session.add(new_score)
    db.session.commit()
    return new_score.to_dict()

@app.route("/rounds/<int:round_id>/scores/<int:id>", methods=["DELETE"])
def score_delete(round_id, id):
    score = db.get_or_404(Score, id)
    db.session.delete(score)
    db.session.commit()
    return ({}, 204)

@app.route("/rounds/<int:round_id>/scores/<int:id>", methods=["PUT"])
def score_update(round_id, id):
    updated_score = request.json
    score = db.get_or_404(Score, id)
    for key in updated_score:
        setattr(score, key, updated_score[key])

    db.session.add(score)
    db.session.commit()
    return score.to_dict()