from functools import wraps
from flask import request, jsonify
import jwt
import datetime

SECRET_KEY = "COMP2001"

def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {"message": "Token is missing"}, 401

        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return {"message": "Token has expired"}, 401
        except jwt.InvalidTokenError:
            return {"message": "Invalid token"}, 401

        request.user_id = decoded_token.get("user_id")
        return func(*args, **kwargs)
    return wrapper

def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if request.user_role != required_role:
                return {"message": "No permission"}, 403
            return func(*args, **kwargs)
        return wrapper
    return decorator