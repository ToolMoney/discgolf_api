from . import app, db
from flask import request
from marshmallow import Schema, fields, EXCLUDE
from flask_login import current_user, login_required


class Disc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    speed = db.Column(db.Integer)
    glide = db.Column(db.Integer)
    turn = db.Column(db.Integer)
    fade = db.Column(db.Integer)
    in_bag = db.Column(db.Boolean)

    user = db.relationship("User", back_populates="discs")


class DiscSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    speed = fields.Int(allow_none=True)
    glide = fields.Int(allow_none=True)
    turn = fields.Int(allow_none=True)
    fade = fields.Int(allow_none=True)
    in_bag = fields.Bool(data_key="inBag")


@app.route("/discs", methods=["GET"])
@login_required
def disc_list():
    discs = db.session.execute(
        db.select(Disc)
        .where(Disc.user_id == current_user.id)
        .order_by(Disc.speed.desc())
    ).scalars()
    schema = DiscSchema(many=True)
    return schema.dump(discs)


@app.route("/discs", methods=["POST"])
@login_required
def disc_add():
    schema = DiscSchema()
    request_data = schema.load(request.json)
    new_disc = Disc(user_id=current_user.id, **request_data)
    db.session.add(new_disc)
    db.session.commit()
    return schema.dump(new_disc)


@app.route("/discs/<int:id>", methods=["DELETE"])
@login_required
def disc_delete(id):
    disc = db.get_or_404(Disc, id)
    db.session.delete(disc)
    db.session.commit()
    return ({}, 204)


@app.route("/discs/<int:id>", methods=["PUT"])
@login_required
def disc_update(id):
    schema = DiscSchema()
    updated_disc = schema.load(request.json)
    disc = db.get_or_404(Disc, id)
    for key in updated_disc:
        setattr(disc, key, updated_disc[key])

    db.session.add(disc)
    db.session.commit()
    return schema.dump(disc)
