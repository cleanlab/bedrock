from backend import app, db
from backend.models import User
from backend.utils import requires_auth

from flask import request, g
from sqlalchemy.orm.exc import NoResultFound


@app.post("/register")
def register():
    data = request.json
    username = data.get("username")
    if not isinstance(username, str):
        return "missing username", 400
    password = data.get("password")
    if not isinstance(password, str):
        return "missing password", 400
    if User.by_username(username) is not None:
        return "already registered", 400
    user = User(username, password)
    db.session.add(user)
    db.session.commit()
    return ""


@app.post("/login")
def login():
    data = request.json
    username = data.get("username")
    if not isinstance(username, str):
        return "missing username", 400
    password = data.get("password")
    if not isinstance(password, str):
        return "missing password", 400
    token = User.login(username, password)
    db.session.commit()
    if not token:
        return "bad username or password", 401
    return {"token": token}


# for debugging
@app.post("/check_token")
def check_token():
    data = request.json
    return {"ok": User.check_token(data.get("username"), data.get("token"))}


@app.route("/status/<username>")
def get_status(username):
    user = User.by_username(username)
    if user is None:
        return "no such user", 404
    return {"status": user.status}


@app.post("/status")
@requires_auth
def set_status():
    status = request.json["status"]
    g.user.status = status
    db.session.commit()
    return ""
