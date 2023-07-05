from . import app, db
from flask import request
from marshmallow import Schema, fields, EXCLUDE


class Disc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    speed = db.Column(db.Integer)
    glide = db.Column(db.Integer)
    turn = db.Column(db.Integer)
    fade = db.Column(db.Integer)
    inBag = db.Column(db.Boolean)


class DiscSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    speed = fields.Int(allow_none=True)
    glide = fields.Int(allow_none=True)
    turn = fields.Int(allow_none=True)
    fade = fields.Int(allow_none=True)
    inBag = fields.Bool()
    

@app.route("/discs", methods=["GET"])
def disc_list():
    discs = db.session.execute(db.select(Disc).order_by(Disc.speed)).scalars()
    schema = DiscSchema(many=True)
    return schema.dump(discs)

@app.route("/discs", methods=["POST"])
def disc_add():
    schema = DiscSchema()
    request_data = schema.load(request.json)
    new_disc = Disc(**request_data)
    db.session.add(new_disc)
    db.session.commit()
    return schema.dump(new_disc)

@app.route("/discs/<int:id>", methods=["DELETE"])
def disc_delete(id):
    disc = db.get_or_404(Disc, id)
    db.session.delete(disc)
    db.session.commit()
    return ({}, 204)

@app.route("/discs/<int:id>", methods=["PUT"])
def disc_update(id):
    schema = DiscSchema()
    updated_disc = schema.load(request.json)
    # TODO inBag case should be snake_case
    disc = db.get_or_404(Disc, id)
    for key in updated_disc:
        setattr(disc, key, updated_disc[key])

    db.session.add(disc)
    db.session.commit()
    return schema.dump(disc)