import base64
from os import environ

from pymongo import MongoClient

from utils import Error4XX

client = MongoClient(
    f"mongodb+srv://{environ['MONGO_USERNAME']}:{environ['MONGO_PASSWORD']}@{environ['MONGO_HOST']}/"
)
db = client['todo-database']
users = db['users']


def add_user(username, password):
    if users.find_one({'username': username}): raise Error4XX('User already exists', 400)
    pass_hash = base64.b64encode(password.encode()).decode()
    user_id = users.insert_one({'username': username, 'password': pass_hash}).inserted_id
    return user_id


def auth_user(username, password):
    pass_hash = base64.b64encode(password.encode()).decode()
    user = users.find_one({'username': username, 'password': pass_hash})
    if not user: raise Error4XX('Invalid username or password', 401)
    return user


def remove_user(username):
    if not users.find_one({'username': username}): raise Error4XX('User does not exist', 404)
    users.delete_one({'username': username})
    return True
