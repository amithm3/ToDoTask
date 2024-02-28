import logging

from flask import Blueprint, jsonify, request

from database import users, add_todo, update_todo, get_todos, remove_todo
from utils import Error4XX, jwt_middleware

app = Blueprint('v1', __name__, url_prefix='/api/v1/')


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


@app.route('/add', methods=['POST'])
@jwt_middleware(users)
def add(user):
    data = request.get_json()
    try:
        todo_id = add_todo(str(user['_id']), data['title'], data['description'], data.get('done', False))
        return jsonify({'_id': str(todo_id)}), 200
    except Error4XX as e:
        return jsonify({'error': str(e)}), e.xx
    except Exception as e:
        logging.error(e)
        return jsonify({'error': "Something went wrong"}), 500


@app.route('/update/<string:todo_id>', methods=['PUT'])
@jwt_middleware(users)
def update(user, todo_id):
    data = request.get_json()
    try:
        update_todo(str(user['_id']), todo_id, **data)
        return jsonify({'status': 'ok'}), 200
    except Error4XX as e:
        return jsonify({'error': str(e)}), e.xx
    except Exception as e:
        logging.error(e)
        return jsonify({'error': "Something went wrong"}), 500


@app.route('/get', methods=['GET'])
@jwt_middleware(users)
def get(user):
    args = request.args
    try:
        todos = get_todos(str(user['_id']), int(args.get('offset', 0)), int(args.get('limit', 10)))
        return jsonify(todos), 200
    except Error4XX as e:
        return jsonify({'error': str(e)}), e.xx
    except Exception as e:
        logging.error(e)
        return jsonify({'error': "Something went wrong"}), 500


@app.route('/delete/<string:todo_id>', methods=['DELETE'])
@jwt_middleware(users)
def delete(user, todo_id):
    try:
        remove_todo(todo_id, str(user['_id']))
        return jsonify({'status': 'ok'}), 200
    except Error4XX as e:
        return jsonify({'error': str(e)}), e.xx
    except Exception as e:
        logging.error(e)
        return jsonify({'error': "Something went wrong"}), 500
