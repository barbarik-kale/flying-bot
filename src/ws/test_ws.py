from unittest import TestCase

from src.drone.services import DroneService
from src.ws.services import TokenService


class TestTokenService(TestCase):
    def setUp(self):
        drone_list_data, error = DroneService.get_drone_list()
        self.assertIsNone(error)
        drone_list = drone_list_data.get('data')
        self.assertGreater(len(drone_list), 0, 'number of drones must be > 0')
        self.drone_id = drone_list[0].get('id')

    def test_get_ws_token(self):
        token = TokenService.get_ws_token('')
        self.assertIsNone(token)

        token = TokenService.get_ws_token(self.drone_id)
        self.assertIsNotNone(token)
