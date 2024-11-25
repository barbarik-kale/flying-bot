import os

from dotenv import load_dotenv

from src.common.util import post, get, put, delete

load_dotenv()
BASE_URL = os.getenv('API_BASE_URL')

class DroneService:

    @staticmethod
    def create_drone(name, avg_speed_ms, flight_time_seconds):
        url = f'{BASE_URL}/drone/'
        body = {
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
    def get_drone(drone_id=None):
        url = f'{BASE_URL}/drone/'
        body = {'drone_id': drone_id}

        response = get(url, body=body)
        # Check if there was an error or status code indicates failure
        if response['error'] or response['status'] is None or not str(response['status']).startswith('2'):
            return None, response['error']
        return response['body'], None

    @staticmethod
    def update_drone(drone_id, data):
        url = f'{BASE_URL}/drone/'
        body = {'drone_id': drone_id, **data}

        response = put(url, body=body)
        # Check if there was an error or status code indicates failure
        if response['error'] or response['status'] is None or not str(response['status']).startswith('2'):
            return None, response['error']
        return response['body'], None

    @staticmethod
    def delete_drone(drone_id):
        url = f'{BASE_URL}/drone/'
        body = {'id': drone_id}

        response = delete(url, body=body)
        # Check if there was an error or status code indicates failure
        if response['error'] or response['status'] is None or not str(response['status']).startswith('2'):
            return None, response['error']
        return response['body'], None

    @staticmethod
    def get_drone_list():
        url = f'{BASE_URL}/drone/list/'

        response = get(url)
        # Check if there was an error or status code indicates failure
        if response['error'] or response['status'] is None or not str(response['status']).startswith('2'):
            return None, response['error']
        return response['body'], None
