from os import environ

from pymongo import MongoClient

client = MongoClient(
    f"mongodb+srv://{environ['MONGO_USERNAME']}:{environ['MONGO_PASSWORD']}@{environ['MONGO_HOST']}/"
)
db = client['todo-database']
users = db['users']


class DBError(Exception):
    pass


def add_user(username, password):
    if users.find_one({'username': username}): raise DBError('User already exists')
    pass_hash = hash(password)
    users.insert_one({'username': username, 'password': pass_hash})
    user = users.find_one({'username': username, 'password': pass_hash})
    return user.get('_id')


def auth_user(username, password):
    pass_hash = hash(password)
    user = users.find_one({'username': username, 'password': pass_hash})
    return user


def remove_user(username):
    try:
        users.delete_one({'username': username})
    except Exception as e:
        raise DBError(e)
    return True
