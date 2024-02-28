import unittest
from pprint import pprint

from app import app
from database import add_user, remove_user


class TestAppAuth(unittest.TestCase):
    USERNAME = "test@test.com"
    PASSWORD = "test@password"

    @classmethod
    def register(cls, client):
        response = client.post(
            '/api/auth/register',
            json={'username': cls.USERNAME, 'password': cls.PASSWORD}
        )
        return response

    @classmethod
    def login(cls, client):
        response = client.post(
            '/api/auth/login',
            json={'username': cls.USERNAME, 'password': cls.PASSWORD}
        )
        return response

    @classmethod
    def delete(cls, token, client):
        response = client.delete(
            '/api/auth/delete',
            headers={'x-access-token': token}
        )
        return response

    def test_register(self):
        with app.test_client() as client:
            response = self.register(client)
            pprint(response.json)
            self.assertEqual(response.status_code, 200)
            remove_user(self.USERNAME)

    def test_register_existing(self):
        with app.test_client() as client:
            add_user(self.USERNAME, self.PASSWORD)
            response = self.register(client)
            pprint(response.json)
            self.assertEqual(response.status_code, 400)
            remove_user(self.USERNAME)

    def test_login(self):
        with app.test_client() as client:
            add_user(self.USERNAME, self.PASSWORD)
            response = self.login(client)
            pprint(response.json)
            self.assertEqual(response.status_code, 200)
            remove_user(self.USERNAME)

    def test_delete(self):
        with app.test_client() as client:
            add_user(self.USERNAME, self.PASSWORD)
            token = self.login(client).json['token']
            response = self.delete(token, client)
            pprint(response.json)
            self.assertEqual(response.status_code, 200)
            response = self.login(client)
            self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
