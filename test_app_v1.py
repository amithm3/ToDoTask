import unittest
from pprint import pprint

import bson

from app import app
from test_app_auth import TestAppAuth

from database import add_user, remove_user, remove_todo


class TestAppV1(unittest.TestCase):
    def test_add_todo(self):
        with app.test_client() as client:
            add_user(TestAppAuth.USERNAME, TestAppAuth.PASSWORD)
            token = TestAppAuth.login(client).json['token']
            response = client.post(
                '/api/v1/add',
                headers={'x-access-token': token},
                json={'title': 'title', 'description': 'description'}
            )
            remove_user(TestAppAuth.USERNAME)
            pprint(response.json)
            self.assertEqual(response.status_code, 200)
            remove_todo(response.json['_id'])

    def test_delete_todo(self):
        with app.test_client() as client:
            add_user(TestAppAuth.USERNAME, TestAppAuth.PASSWORD)
            token = TestAppAuth.login(client).json['token']
            response = client.post(
                '/api/v1/add',
                headers={'x-access-token': token},
                json={'title': 'title', 'description': 'description'}
            )
            response = client.delete(
                f'/api/v1/delete/{response.json["_id"]}',
                headers={'x-access-token': token}
            )
            remove_user(TestAppAuth.USERNAME)
            pprint(response.json)
            self.assertEqual(response.status_code, 200)

    def test_delete_todo_invalid_id(self):
        with app.test_client() as client:
            add_user(TestAppAuth.USERNAME, TestAppAuth.PASSWORD)
            token = TestAppAuth.login(client).json['token']
            response = client.delete(
                f'/api/v1/delete/{bson.ObjectId()}',
                headers={'x-access-token': token}
            )
            remove_user(TestAppAuth.USERNAME)
            pprint(response.json)
            self.assertEqual(response.status_code, 404)

    def test_get_todos(self):
        with app.test_client() as client:
            add_user(TestAppAuth.USERNAME, TestAppAuth.PASSWORD)
            token = TestAppAuth.login(client).json['token']
            response = client.get(
                '/api/v1/get?offset=0&limit=10',
                headers={'x-access-token': token}
            )
            remove_user(TestAppAuth.USERNAME)
            pprint(response.json)
            self.assertEqual(response.status_code, 200)

    def test_update_todo(self):
        with app.test_client() as client:
            add_user(TestAppAuth.USERNAME, TestAppAuth.PASSWORD)
            token = TestAppAuth.login(client).json['token']
            todo_id = client.post(
                '/api/v1/add',
                headers={'x-access-token': token},
                json={'title': 'title', 'description': 'description'}
            ).json['_id']
            response = client.put(
                f'/api/v1/update/{todo_id}',
                headers={'x-access-token': token},
                json={'title': 'title', 'description': 'description', 'done': True}
            )
            remove_user(TestAppAuth.USERNAME)
            pprint(response.json)
            self.assertEqual(response.status_code, 200)
            remove_todo(todo_id)


if __name__ == '__main__':
    unittest.main()
