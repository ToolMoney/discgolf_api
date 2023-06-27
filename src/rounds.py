from . import app, db
from flask import request


class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    # user = db.Column()
    default_layout = db.Column(db.String)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    scores = db.relationship("Score", back_populates="round")
    course = db.relationship("Course", back_populates="rounds")


    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            # "user": self.user,
            "default_layout": self.default_layout,
            "course_id": self.course_id,
            "scores": [score.to_dict() for score in self.scores],
            }
    

with app.app_context():
    db.create_all()


@app.route("/rounds", methods=["GET"])
def round_list():
    rounds = db.session.execute(db.select(Round).order_by(Round.date.desc())).scalars()
    return [round.to_dict() for round in rounds]

@app.route("/rounds", methods=["POST"])
def round_add():
    # new_hole = Hole(course_id=course_id, **request.json)
    new_round = Round(**request.json)
    db.session.add(new_round)
    db.session.commit()
    return new_round.to_dict()

@app.route("/rounds/<int:id>", methods=["DELETE"])
def round_delete(id):
    round = db.get_or_404(Round, id)
    db.session.delete(round)
    db.session.commit()
    return ({}, 204)

@app.route("/rounds/<int:id>", methods=["PUT"])
def round_update(id):
    updated_round = request.json
    round = db.get_or_404(Round, id)
    for key in updated_round:
        setattr(round, key, updated_round[key])

    db.session.add(round)
    db.session.commit()
    return round.to_dict()


@app.route("/rounds/<int:id>", methods=["GET"])
def round_details(id):
    round = db.session.execute(db.select(Round).where(Round.id == id)).scalar()
    return round.to_dict()