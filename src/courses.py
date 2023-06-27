from . import app, db
from flask import request


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String)
    fee = db.Column(db.Integer)
    favorite = db.Column(db.Boolean)

    holes = db.relationship("Hole", back_populates="course", order_by="(Hole.hole_number.asc(), nulls_last(Hole.layout.asc()))")
    rounds = db.relationship("Round", back_populates="course", order_by="(Round.date.desc())")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "fee": self.fee,
            "favorite": self.favorite,
            "holes": [hole.to_dict() for hole in self.holes],
            "rounds": [round.to_dict() for round in self.rounds],
            }



with app.app_context():
    db.create_all()


@app.route("/courses", methods=["GET"])
def course_list():
    courses = db.session.execute(db.select(Course).order_by(Course.favorite.desc())).scalars()
    return [course.to_dict() for course in courses]

@app.route("/courses", methods=["POST"])
def course_add():
    new_course = Course(**request.json)
    db.session.add(new_course)
    db.session.commit()
    return new_course.to_dict()

@app.route("/courses/<int:id>", methods=["DELETE"])
def course_delete(id):
    course = db.get_or_404(Course, id)
    db.session.delete(course)
    db.session.commit()
    return ({}, 204)

@app.route("/courses/<int:id>", methods=["PUT"])
def course_update(id):
    updated_course = request.json
    course = db.get_or_404(Course, id)
    for key in updated_course:
        setattr(course, key, updated_course[key])

    db.session.add(course)
    db.session.commit()
    return course.to_dict()


@app.route("/courses/<int:id>", methods=["GET"])
def course_details(id):
    course = db.session.execute(db.select(Course).where(Course.id == id)).scalar()
    return course.to_dict()
