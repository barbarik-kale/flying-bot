import os

from src.common.util import post

BASE_URL = os.getenv('API_BASE_URL')

class TokenService():
    @staticmethod
    def get_ws_token(drone_id):
        url = f'{BASE_URL}/ws/token/'
        body = {'drone_id': str(drone_id)}
        response = post(url, body=body)
        if response['error'] or response['status'] is None or not str(response['status']).startswith('2'):
            return None
        body = response['body']
        return body.get('data', {}).get('token')
