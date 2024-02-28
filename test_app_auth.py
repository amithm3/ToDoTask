import unittest
from pprint import pprint

from app import app
from database import remove_user

from utils import random_string, Error4XX


class TestAppAuth(unittest.TestCase):
    class Register:
        def __init__(self, username, password, client):
            self.username = username
            self.password = password
            self.client = client
            self.user_id = None

        def __enter__(self):
            response = TestAppAuth.register(self.username, self.password, self.client)
            self.user_id = response.json['_id']
            return response

        def __exit__(self, exc_type, exc_val, exc_tb):
            remove_user(self.user_id)
            self.user_id = None

    @staticmethod
    def register(username, password, client):
        response = client.post(
            '/api/auth/register',
            json={'username': username, 'password': password}
        )
        return response

    @staticmethod
    def login(username, password, client):
        response = client.post(
            '/api/auth/login',
            json={'username': username, 'password': password}
        )
        return response

    @staticmethod
    def delete(token, client):
        response = client.delete(
            '/api/auth/delete',
            headers={'x-access-token': token}
        )
        return response

    def test_register(self):
        with app.test_client() as client, self.Register(random_string(8), random_string(16), client) as response:
            pprint(response.json)
            self.assertEqual(response.status_code, 200)

    def test_register_existing(self):
        username = random_string(8)
        password = random_string(16)
        with app.test_client() as client, self.Register(username, password, client) as response:
            pprint(response.json)
            self.assertEqual(response.status_code, 200)
            response = self.register(username, password, client)
            pprint(response.json)
            self.assertEqual(response.status_code, 400)

    def test_login(self):
        username = random_string(8)
        password = random_string(16)
        with app.test_client() as client, self.Register(username, password, client) as response:
            pprint(response.json)
            response = self.login(username, password, client)
            pprint(response.json)
            self.assertEqual(response.status_code, 200)

    def test_delete(self):
        username = random_string(8)
        password = random_string(16)
        try:
            with app.test_client() as client, self.Register(username, password, client) as response:
                pprint(response.json)
                response = self.login(username, password, client)
                pprint(response.json)
                token = response.json['token']
                response = self.delete(token, client)
                pprint(response.json)
                self.assertEqual(response.status_code, 200)
        except Error4XX as e:
            self.assertEqual(e.xx, 404)


if __name__ == '__main__':
    unittest.main()
