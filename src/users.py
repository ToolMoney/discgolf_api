from . import app, db, bcrypt, login_manager
from flask import request
from marshmallow import Schema, fields, EXCLUDE
from flask_login import UserMixin, login_user, current_user


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    pass_hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)


class UserSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    password = fields.Str(load_only=True)
    email = fields.Str()



@app.route("/users", methods=["POST"])
def user_add():
    schema = UserSchema()
    request_data = schema.load(request.json)

    pw_hash = bcrypt.generate_password_hash(request_data['password']).decode('utf-8')
    request_data['pass_hash'] = pw_hash
    del request_data['password']

    new_user = User(**request_data)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return schema.dump(new_user)

@app.route("/users/login", methods=["POST"])
def login():
    schema = UserSchema()
    request_data = schema.load(request.json)
    name = request_data['name']
    user = db.session.execute(db.select(User).where(User.name == name)).scalar()
    if bcrypt.check_password_hash(user.pass_hash, request_data['password']):
        login_user(user)
        return schema.dump(user)
    raise Exception('your password does not match a user by that name')

@app.route("/users/self", methods=["GET"])
def user_get():
    schema = UserSchema()
    print(current_user)
    return schema.dump(current_user)

@login_manager.user_loader
def load_user(user_id):
    user = db.session.execute(db.select(User).where(User.id == user_id)).scalar()
    return user