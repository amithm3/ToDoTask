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
users = db['users']
todos = db['todos']


def add_user(username: str, password: str):
    if users.find_one({'username': username}): raise Error4XX('User already exists', 400)
    pass_hash = base64.b64encode(password.encode()).decode()
    user_id = users.insert_one({'username': username, 'password': pass_hash}).inserted_id
    return user_id


def auth_user(username: str, password: str):
    pass_hash = base64.b64encode(password.encode()).decode()
    user = users.find_one({'username': username, 'password': pass_hash})
    if not user: raise Error4XX('Invalid username or password', 401)
    return user


def remove_user(username: str):
    if not users.find_one({'username': username}): raise Error4XX('User does not exist', 404)
    users.delete_one({'username': username})
    return True


def add_todo(user_id: str, title: str, description: str, done: bool = False):
    user = get_user_by_id(user_id)
    if not user: raise Error4XX('User does not exist', 404)
    todo_id = todos.insert_one({
        'user_id': user_id,
        'title': title,
        'description': description,
        'done': done,
        'timestamp': time.time()
    }).inserted_id
    return todo_id


def get_todos(user_id: str, offset: int = 0, limit: int = 10):
    user = get_user_by_id(user_id)
    if not user: raise Error4XX('User does not exist', 404)
    return list(todos.find({'user_id': user_id}).sort('timestamp', -1).skip(offset).limit(limit))


def remove_todo(todo_id: str, user_id: str = None):
    todo = todos.find_one({'_id': ObjectId(todo_id)})
    if not todo: raise Error4XX('Todo does not exist', 404)
    if user_id:
        user = users.find_one({'_id': ObjectId(user_id)})
        if not user: raise Error4XX('User does not exist', 404)
        if todo['user_id'] != user_id: raise Error4XX('Unauthorized', 401)
    todos.delete_one({'_id': ObjectId(todo_id)})
    return True


def update_todo(user_id: str, todo_id: str, **kwargs):
    user = get_user_by_id(user_id)
    todo = get_todo_by_id(todo_id)
    if not user: raise Error4XX('User does not exist', 404)
    if not todo: raise Error4XX('Todo does not exist', 404)
    if todo['user_id'] != user_id: raise Error4XX('Unauthorized', 401)
    todos.update_one({'_id': todo_id}, {'$set': kwargs})
    return True


def get_user_by_username(username):
    return users.find_one({'username': username})


def get_user_by_id(user_id):
    return users.find_one({'_id': ObjectId(user_id)})


def get_todo_by_id(todo_id):
    return todos.find_one({'_id': ObjectId(todo_id)})
