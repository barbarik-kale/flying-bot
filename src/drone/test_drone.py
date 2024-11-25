from unittest import TestCase

from src.drone.services import DroneService


class TestDrone(TestCase):

    def test_create_and_get_drone(self):
        data, error = DroneService.create_drone('test', 10, 1000)
        self.assertIsNotNone(data)
        drone_id = data.get('data').get('id')
        self.assertIsNotNone(drone_id)

        drone, error = DroneService.get_drone(drone_id)
        self.assertIsNone(error)
        self.assertIsNotNone(drone)
        self.assertEqual(drone_id, drone.get('data').get('id'))

        data, error = DroneService.delete_drone(drone_id)
        self.assertIsNotNone(data)
        self.assertIsNone(error)

    def test_get_list(self):
        data, error = DroneService.get_drone_list()
        self.assertIsNone(error)
        self.assertIsNotNone(data.get('data'))

