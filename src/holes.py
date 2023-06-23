from . import app, db
from flask import request


class Hole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hole_number = db.Column(db.Integer)
    par = db.Column(db.Integer)
    layout = db.Column(db.String)
    distance = db.Column(db.Integer)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    course = db.relationship("Course", back_populates="holes")

    def to_dict(self):
        return {
            "id": self.id,
            "hole_number": self.hole_number,
            "par": self.par,
            "layout": self.layout,
            "distance": self.distance,
            "course_id": self.course_id,
        }



with app.app_context():
    db.create_all()


@app.route("/courses/<int:course_id>", methods=["POST"])
def hole_add(course_id):
    new_hole = Hole(course_id=course_id, **request.json)
    db.session.add(new_hole)
    db.session.commit()
    return new_hole.to_dict()

@app.route("/courses/<int:course_id>/<int:id>", methods=["DELETE"])
def hole_delete(course_id, id):
    hole = db.get_or_404(Hole, id)
    db.session.delete(hole)
    db.session.commit()
    return ({}, 204)

@app.route("/courses/<int:course_id>/<int:id>", methods=["PUT"])
def hole_update(course_id, id):
    updated_hole = request.json
    hole = db.get_or_404(Hole, id)
    for key in updated_hole:
        setattr(hole, key, updated_hole[key])

    db.session.add(hole)
    db.session.commit()
    return hole.to_dict()