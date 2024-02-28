import logging
from functools import wraps
from os import environ

from flask import Blueprint, jsonify, request
import jwt

from database import add_user, remove_user, auth_user, users, DBError

app = Blueprint('v1', __name__, url_prefix='/api/v1')


def jwt_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers: token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401
        try:
            data = jwt.decode(token, environ["JWT_SECRET"], algorithms=["HS256"])
            current_user = users.find_one({'username': data['username']})
        except Exception as e:
            logging.error(e)
            return jsonify({'error': "could not validate token"}), 401
        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        user_id = add_user(data['username'], data['password'])
        return jsonify({'id': str(user_id)}), 200
    except DBError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logging.error(e)
        return jsonify({'error': "Something went wrong"}), 500


@app.route('/delete', methods=['DELETE'])
@jwt_token
def delete(current_user):
    try:
        remove_user(current_user['username'])
        return jsonify({'status': 'ok'}), 200
    except DBError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logging.error(e)
        return jsonify({'error': "Something went wrong"}), 500


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        user = auth_user(data['username'], data['password'])
        if user:
            token = jwt.encode({'username': user['username']}, environ["JWT_SECRET"], algorithm="HS256")
            return jsonify({'token': token}), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    except Exception as e:
        logging.error(e)
        return jsonify({'error': "Something went wrong"}), 500
