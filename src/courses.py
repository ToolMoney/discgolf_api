from . import app, db
from flask import request
from marshmallow import Schema, fields, EXCLUDE
from .holes import HoleSchema
from .rounds import RoundSchema
from flask_login import current_user


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String)
    fee = db.Column(db.Integer)
    favorite = db.Column(db.Boolean)

    user = db.relationship("User", back_populates="courses")
    holes = db.relationship(
        "Hole",
        back_populates="course",
        order_by="(Hole.hole_number.asc(), nulls_last(Hole.layout.asc()))",
        cascade="all, delete-orphan"
    )
    rounds = db.relationship(
        "Round",
        back_populates="course",
        order_by="(Round.date.desc())",
        cascade="all, delete-orphan"
    )


class CourseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    location = fields.Str(allow_none=True)
    fee = fields.Int(allow_none=True)
    favorite = fields.Bool()
    holes = fields.List(fields.Nested(HoleSchema))
    rounds = fields.List(fields.Nested(RoundSchema))


@app.route("/courses", methods=["GET"])
def course_list():
    courses = db.session.execute(
        db.select(Course)
        .where(Course.user_id == current_user.id)
        .order_by(Course.favorite.desc())
    ).scalars()
    return CourseSchema(many=True).dump(courses)


@app.route("/courses", methods=["POST"])
def course_add():
    schema = CourseSchema()
    request_data = schema.load(request.json)
    new_course = Course(user_id=current_user.id, **request_data)
    db.session.add(new_course)
    db.session.commit()
    return schema.dump(new_course)


@app.route("/courses/<int:id>", methods=["DELETE"])
def course_delete(id):
    course = db.get_or_404(Course, id)
    db.session.delete(course)
    db.session.commit()
    return ({}, 204)


@app.route("/courses/<int:id>", methods=["PUT"])
def course_update(id):
    schema = CourseSchema()
    updated_course = schema.load(request.json)
    course = db.get_or_404(Course, id)
    for key in updated_course:
        setattr(course, key, updated_course[key])

    db.session.add(course)
    db.session.commit()
    return schema.dump(course)


@app.route("/courses/<int:id>", methods=["GET"])
def course_details(id):
    course = db.session.execute(db.select(Course).where(Course.id == id)).scalar()
    return CourseSchema().dump(course)
