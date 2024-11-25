from unittest import TestCase
from uuid import uuid4

from dotenv import load_dotenv

from src.user.services import UserService


class TestUser(TestCase):
    def setUp(self):
        load_dotenv()
        self.password = str(uuid4())
        self.email = f'test_{self.password}@mail.com'

    def test_all(self):
        data = UserService.login_user(self.email, self.password)
        self.assertIsNone(data)

        data = UserService.register_user(self.email, self.password)
        self.assertIsNotNone(data)

        data = UserService.login_user(self.email, self.password)
        self.assertIsNotNone(data)
        self.assertIsNotNone(data.get('token'))

        data = UserService.register_user(self.email, self.password)
        self.assertIsNone(data)
