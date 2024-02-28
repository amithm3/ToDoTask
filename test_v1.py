import unittest
from pprint import pprint

from app import app
from database import remove_user, add_user


class TestV1(unittest.TestCase):
    @classmethod
    def create_and_login(cls, username, password, client):
        add_user(username, password)
        return cls.login(username, password, client)

    @classmethod
    def login(cls, username, password, client):
        response = client.post(
            '/api/v1/login',
            json={'username': username, 'password': password}
        )
        return response

    def test_register(self):
        with app.test_client() as client:
            username = "test@test.text"
            password = "test@password"
            response = client.post(
                '/api/v1/register',
                json={'username': username, 'password': password}
            )
            pprint(response.json)
            self.assertEqual(response.status_code, 200)
            remove_user(username)

    def test_register_existing(self):
        with app.test_client() as client:
            username = "test@test.text"
            password = "test@password"
            response = client.post(
                '/api/v1/register',
                json={'username': username, 'password': password}
            )
            self.assertEqual(response.status_code, 200)
            response = client.post(
                '/api/v1/register',
                json={'username': username, 'password': password}
            )
            self.assertEqual(response.status_code, 400)
            remove_user(username)

    def test_login(self):
        with app.test_client() as client:
            username = "test@test.text"
            password = "test@password"
            add_user(username, password)
            response = client.post(
                '/api/v1/login',
                json={'username': username, 'password': password}
            )
            pprint(response.json)
            self.assertEqual(response.status_code, 200)
            remove_user(username)

    def test_delete(self):
        with app.test_client() as client:
            username = "test@test.test"
            password = "test@password"
            token = self.create_and_login(username, password, client).json['token']
            response = client.delete(
                '/api/v1/delete',
                headers={'x-access-token': token}
            )
            pprint(response.json)
            self.assertEqual(response.status_code, 200)
            response = self.login(username, password, client)
            self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
