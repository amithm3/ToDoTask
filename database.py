import base64
import time
from os import environ

from bson import ObjectId
from pymongo import MongoClient

from utils import Error4XX

client = MongoClient(
    f"mongodb+srv://{environ['MONGO_USERNAME']}:{environ['MONGO_PASSWORD']}@{environ['MONGO_HOST']}/"
)
db = client['todo-database']
user_col = db['users']
todo_col = db['todos']


def add_user(username: str, password: str) -> str:
    assert isinstance(username, str) and len(username) >= 4, 'Username must be at least 4 characters long'
    assert isinstance(password, str) and len(password) >= 8, 'Password must be at least 8 characters long'
    if user_col.find_one({'username': username}): raise Error4XX('User already exists', 400)
    encodes_pass = base64.b64encode(password.encode()).decode()
    user_id = user_col.insert_one({'username': username, 'password': encodes_pass}).inserted_id
    return str(user_id)


def auth_user(username: str, password: str):
    assert isinstance(username, str)
    assert isinstance(password, str)
    encodes_pass = base64.b64encode(password.encode()).decode()
    user = user_col.find_one({'username': username, 'password': encodes_pass})
    if not user: raise Error4XX('Invalid username or password', 401)
    return str(user['_id'])


def remove_user(user_id: str):
    assert isinstance(user_id, str)
    user_id = ObjectId(user_id)
    if not user_col.find_one({'_id': user_id}): raise Error4XX('User does not exist', 404)
    deleted = user_col.delete_one({'_id': user_id})
    return bool(deleted.deleted_count)


def add_todo(user_id: str, title: str, description: str, done: bool = False):
    assert isinstance(user_id, str)
    assert isinstance(title, str)
    assert isinstance(description, str)
    assert isinstance(done, bool)
    user = get_user_by_id(user_id)
    user_id = ObjectId(user_id)
    if not user: raise Error4XX('User does not exist', 404)
    todo_id = todo_col.insert_one({
        'user_id': user_id,
        'title': title,
        'description': description,
        'done': done,
        'timestamp': time.time()
    }).inserted_id
    return todo_id


def get_todos(user_id: str, offset: int = 0, limit: int = 0):
    user = get_user_by_id(user_id)
    user_id = ObjectId(user_id)
    if not user: raise Error4XX('User does not exist', 404)
    todos = todo_col.find({'user_id': user_id}).sort('timestamp', -1).skip(offset).limit(limit)
    return list(map(lambda todo: {**todo, '_id': str(todo['_id']), "user_id": str(todo['user_id'])}, todos))


def remove_todo(todo_id: str, user_id: str = None):
    todo = get_todo_by_id(todo_id)
    todo_id = ObjectId(todo_id)
    if not todo: raise Error4XX('Todo does not exist', 404)
    if user_id:
        user = get_user_by_id(user_id)
        user_id = ObjectId(user_id)
        if not user: raise Error4XX('User does not exist', 404)
        if todo['user_id'] != user_id: raise Error4XX('Unauthorized', 401)
    deleted = todo_col.delete_one({'_id': todo_id})
    return bool(deleted.deleted_count)


def update_todo(todo_id: str, user_id: str = None, **kwargs):
    todo = get_todo_by_id(todo_id)
    if not todo: raise Error4XX('Todo does not exist', 404)
    if user_id:
        user = get_user_by_id(user_id)
        user_id = ObjectId(user_id)
        if not user: raise Error4XX('User does not exist', 404)
        if todo['user_id'] != user_id: raise Error4XX('Unauthorized', 401)
    updated = todo_col.update_one({'_id': todo_id}, {'$set': kwargs})
    return bool(updated.modified_count)


def get_user_by_username(username):
    return user_col.find_one({'username': username})


def get_user_by_id(user_id):
    return user_col.find_one({'_id': ObjectId(user_id)})


def get_todo_by_id(todo_id):
    return todo_col.find_one({'_id': ObjectId(todo_id)})
