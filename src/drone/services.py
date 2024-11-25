import os

from src.common.util import post, get, put, delete

BASE_URL = os.getenv('API_BASE_URL')

class DroneService:

    @staticmethod
    def create_drone(email, name, avg_speed_ms, flight_time_seconds):
        url = f'{BASE_URL}/create_drone/'
        body = {
            'email': email,
            'name': name,
            'avg_speed_ms': avg_speed_ms,
            'flight_time_seconds': flight_time_seconds
        }

        response = post(url, body=body)
        # Check if there was an error or status code indicates failure
        if response['error'] or response['status'] is None or not str(response['status']).startswith('2'):
            return None, response['error']
        return response['body'], None

    @staticmethod
    def get_drone(email, drone_id=None):
        url = f'{BASE_URL}/get_drone/'
        params = {'email': email, 'drone_id': drone_id}

        response = get(url, params=params)
        # Check if there was an error or status code indicates failure
        if response['error'] or response['status'] is None or not str(response['status']).startswith('2'):
            return None, response['error']
        return response['body'], None

    @staticmethod
    def update_drone(email, drone_id, data):
        url = f'{BASE_URL}/update_drone/'
        body = {'email': email, 'drone_id': drone_id, **data}

        response = put(url, body=body)
        # Check if there was an error or status code indicates failure
        if response['error'] or response['status'] is None or not str(response['status']).startswith('2'):
            return None, response['error']
        return response['body'], None

    @staticmethod
    def delete_drone(email, drone_id):
        url = f'{BASE_URL}/delete_drone/'
        params = {'email': email, 'drone_id': drone_id}

        response = delete(url, params=params)
        # Check if there was an error or status code indicates failure
        if response['error'] or response['status'] is None or not str(response['status']).startswith('2'):
            return None, response['error']
        return response['body']['id'], None

    @staticmethod
    def get_drone_list(email):
        url = f'{BASE_URL}/get_drone_list/'
        params = {'email': email}

        response = get(url, params=params)
        # Check if there was an error or status code indicates failure
        if response['error'] or response['status'] is None or not str(response['status']).startswith('2'):
            return None, response['error']
        return response['body'], None
