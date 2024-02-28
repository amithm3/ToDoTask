import unittest
from pprint import pprint

import bson

from app import app
from test_app_auth import TestAppAuth

from database import remove_todo, get_todos
from utils import random_string


class TestAppV1(unittest.TestCase):
    class Register(TestAppAuth.Register):
        def __enter__(self):
            super().__enter__()
            return TestAppAuth.login(self.username, self.password, self.client)

        def __exit__(self, exc_type, exc_val, exc_tb):
            [remove_todo(todo['_id']) for todo in get_todos(self.user_id)]
            super().__exit__(exc_type, exc_val, exc_tb)

    @classmethod
    def add(cls, token, client):
        response = client.post(
            '/api/v1/add',
            headers={'x-access-token': token},
            json={'title': random_string(16), 'description': random_string(64)}
        )
        return response

    def test_add(self):
        with app.test_client() as client, self.Register(random_string(16), random_string(16), client) as response:
            pprint(response.json)
            response = self.add(response.json['token'], client)
            pprint(response.json)
            self.assertEqual(response.status_code, 200)

    def test_delete_todo(self):
        with app.test_client() as client, self.Register(random_string(16), random_string(16), client) as response:
            pprint(response.json)
            token = response.json['token']
            todo = self.add(token, client).json
            response = client.delete(
                f'/api/v1/delete/{todo["_id"]}',
                headers={'x-access-token': token}
            )
            pprint(response.json)
            self.assertEqual(response.status_code, 200)

    def test_delete_todo_invalid_id(self):
        with app.test_client() as client, self.Register(random_string(16), random_string(16), client) as response:
            pprint(response.json)
            token = response.json['token']
            response = client.delete(
                f'/api/v1/delete/{bson.ObjectId()}',
                headers={'x-access-token': token}
            )
            pprint(response.json)
            self.assertEqual(response.status_code, 404)

    def test_delete_todo_invalid_user(self):
        with (app.test_client() as client,
              self.Register(random_string(16), random_string(16), client) as response1,
              self.Register(random_string(16), random_string(16), client) as response2):
            pprint(response1.json)
            pprint(response2.json)
            token1 = response1.json['token']
            token2 = response2.json['token']
            todo = self.add(token1, client).json
            response = client.delete(
                f'/api/v1/delete/{todo["_id"]}',
                headers={'x-access-token': token2}
            )
            pprint(response.json)
            self.assertEqual(response.status_code, 401)

    def test_get_todos(self):
        with app.test_client() as client, self.Register(random_string(16), random_string(16), client) as response:
            pprint(response.json)
            token = response.json['token']
            [self.add(token, client) for _ in range(10)]
            response = client.get(
                '/api/v1/get?offset=3&limit=5',
                headers={'x-access-token': token}
            )
            pprint(response.json)
            self.assertEqual(response.status_code, 200)

    def test_update_todo(self):
        with app.test_client() as client, self.Register(random_string(16), random_string(16), client) as response:
            pprint(response.json)
            token = response.json['token']
            response = self.add(token, client)
            pprint(response.json)
            response = client.put(
                f'/api/v1/update/{response.json["_id"]}',
                headers={'x-access-token': token},
                json={'done': True}
            )
            pprint(response.json)
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
