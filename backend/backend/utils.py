from backend.models.user import User

from flask import request, g

from functools import wraps


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "Authorization" in request.headers:
            auth = request.headers["Authorization"]
            _, token = auth.split()  # expected to be 'Bearer <token>'
            user = User.by_token(token)
            if user is not None:
                print(f"user is: {user}")
                g.user = user
                return f(*args, **kwargs)
        return "requires auth", 401

    return decorated
