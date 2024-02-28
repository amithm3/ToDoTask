import logging
from functools import wraps
from os import environ

import jwt
from bson import ObjectId
from flask import request, jsonify


def jwt_token(users):
    def decorator(foo):
        @wraps(foo)
        def wrapper(*args, **kwargs):
            token = None
            if 'x-access-token' in request.headers: token = request.headers['x-access-token']
            if not token: return jsonify({'message': 'Token is missing !!'}), 401
            try:
                data = jwt.decode(token, environ["JWT_SECRET"], algorithms=["HS256"])
                user = users.find_one({'_id': ObjectId(data['_id'])})
            except Exception as e:
                logging.error(e)
                return jsonify({'error': "could not validate token"}), 401
            return foo(user, *args, **kwargs)

        return wrapper

    return decorator


class Error4XX(Exception):
    def __init__(self, message="", xx=400):
        super().__init__(message)
        self.xx = xx
