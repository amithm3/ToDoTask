import logging
from os import environ

import jwt
from flask import Blueprint, jsonify, request

from database import add_user, auth_user, remove_user, users
from utils import jwt_token, Error4XX

app = Blueprint('auth', __name__, url_prefix='/api/auth/')


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        user_id = add_user(data['username'], data['password'])
        return jsonify({'_id': str(user_id)}), 200
    except Error4XX as e:
        return jsonify({'error': str(e)}), e.xx
    except Exception as e:
        logging.error(e)
        return jsonify({'error': "Something went wrong"}), 500


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        user = auth_user(data['username'], data['password'])
        token = jwt.encode({'_id': str(user["_id"])}, environ["JWT_SECRET"], algorithm="HS256")
        return jsonify({'token': token}), 200
    except Error4XX as e:
        return jsonify({'error': str(e)}), e.xx
    except Exception as e:
        logging.error(e)
        return jsonify({'error': "Something went wrong"}), 500


@app.route('/delete', methods=['DELETE'])
@jwt_token(users)
def delete(user):
    try:
        remove_user(user['username'])
        return jsonify({'status': 'ok'}), 200
    except Error4XX as e:
        return jsonify({'error': str(e)}), e.xx
    except Exception as e:
        logging.error(e)
        return jsonify({'error': "Something went wrong"}), 500
