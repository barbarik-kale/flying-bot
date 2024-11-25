import os
from unittest import TestCase
from uuid import uuid4

from src.user.services import UserService


class TestUser(TestCase):
    def setUp(self):
        self.password = str(uuid4())
        self.email = f'test_{self.password}@mail.com'

    def test_login_register_flow(self):
        data = UserService.login_user(self.email, self.password)
        self.assertIsNone(data)

        data = UserService.register_user(self.email, self.password)
        self.assertIsNotNone(data)

        data = UserService.login_user(self.email, self.password)
        self.assertIsNotNone(data)
        self.assertIsNotNone(data.get('data').get('token'))

        data = UserService.register_user(self.email, self.password)
        self.assertIsNone(data)

class TestUserList(TestCase):
    def setUp(self):
        self.email = 'test@email.com'
        self.password = 'test'
        data = UserService.register_user(self.email, self.password)

        data = UserService.login_user(self.email, self.password)
        self.assertIsNotNone(data)
        token = data.get('data').get('token')
        self.assertIsNotNone(token)

        os.environ['AUTH_TOKEN'] = token

    def test_user_list(self):
        data = UserService.list_users()
        self.assertIsNotNone(data)