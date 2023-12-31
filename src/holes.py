from . import app, db
from flask import request
from marshmallow import Schema, fields, EXCLUDE
from flask_login import current_user, login_required


class Hole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    hole_number = db.Column(db.Integer)
    par = db.Column(db.Integer)
    layout = db.Column(db.String)
    distance = db.Column(db.Integer)

    user = db.relationship("User")
    course = db.relationship("Course", back_populates="holes")
    scores = db.relationship(
        "Score", back_populates="hole",
        order_by="(Score.score.desc())",
        cascade="all, delete-orphan"
    )


class HoleSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    hole_number = fields.Int(allow_none=True)
    par = fields.Int(allow_none=True)
    layout = fields.Str(allow_none=True)
    distance = fields.Int(allow_none=True)
    course_id = fields.Int(required=True)


@app.route("/courses/<int:course_id>", methods=["POST"])
@login_required
def hole_add(course_id):
    schema = HoleSchema()
    request_data = schema.load({"course_id": course_id, **request.json})
    new_hole = Hole(user_id=current_user.id, **request_data)
    db.session.add(new_hole)
    db.session.commit()
    return schema.dump(new_hole)


@app.route("/courses/<int:course_id>/<int:id>", methods=["DELETE"])
@login_required
def hole_delete(course_id, id):
    hole = db.get_or_404(Hole, id)
    db.session.delete(hole)
    db.session.commit()
    return ({}, 204)


@app.route("/courses/<int:course_id>/<int:id>", methods=["PUT"])
@login_required
def hole_update(course_id, id):
    schema = HoleSchema()
    updated_hole = schema.load(request.json)
    hole = db.get_or_404(Hole, id)
    for key in updated_hole:
        setattr(hole, key, updated_hole[key])

    db.session.add(hole)
    db.session.commit()
    return schema.dump(hole)
