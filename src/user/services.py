import os

from src.common.util import post, get

BASE_URL = os.getenv('API_BASE_URL')

class UserService:

    @staticmethod
    def register_user(email, password):
        url = f'{BASE_URL}/user/register/'
        body = {'email': email, 'password': password}

        response = post(url, body=body)
        # Check if there was an error or status code indicates failure
        if response['error'] or response['status'] is None or not str(response['status']).startswith('2'):
            return None
        return response['body']

    @staticmethod
    def login_user(email, password):
        url = f'{BASE_URL}/user/login/'
        body = {'email': email, 'password': password}

        response = post(url, body=body)
        # Check if there was an error or status code indicates failure
        if response['error'] or response['status'] is None or not str(response['status']).startswith('2'):
            return None
        return response['body']

    @staticmethod
    def list_users():
        url = f'{BASE_URL}/user/user-list/'

        response = get(url)
        # Check if there was an error or status code indicates failure
        if response['error'] or response['status'] is None or not str(response['status']).startswith('2'):
            return None
        return response['body']
