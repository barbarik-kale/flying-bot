import asyncio
import json
import os

import websockets

from src.drone.services import DroneService

SEND_INTERVAL = 5

class Drone:
    """
    Simulates a drone bot.
    """
    def __init__(self, drone_id):
        drone_details, error = DroneService.get_drone(drone_id)
        drone_details = drone_details.get('data')
        self.id = drone_details.get('id')
        self.name = drone_details.get('name')
        self.avg_speed_ms = drone_details.get('avg_speed_ms')
        self.token = os.getenv('AUTH_TOKEN')
        self.uri = os.getenv('DRONE_WS_URI')
        self.latitude = 0
        self.longitude = 0
        self.websocket = None

    def __handle_message(self, message):
        try:
            message = json.loads(message)
            command = message.get('command')
            if command == 'LEFT':
                self.latitude -= self.avg_speed_ms
            elif command == 'RIGHT':
                self.latitude += self.avg_speed_ms
            elif command == 'UP':
                self.longitude += self.avg_speed_ms
            elif command == 'DOWN':
                self.longitude -= self.longitude
        except Exception as e:
            pass

    async def __connect(self, uri):
        uri = f'{uri}?drone_id={self.id}'
        headers = {
            'Authorization': self.token
        }
        try:
            self.websocket = await websockets.connect(uri, additional_headers=headers)
            print(f'Drone {self.id} connected to {uri}')
        except Exception as e:
            print(f'Error connecting drone {self.id}: {e}')

    async def __send(self, data):
        if self.websocket:
            try:
                await self.websocket.send(data)
                print(f'Data sent from drone {self.id}: {data}')
            except Exception as e:
                print(f'Error sending data: {e}')
        else:
            print('Not connected to the server.')

    async def __receive(self):
        try:
            async for message in self.websocket:
                self.__handle_message(message)
        except Exception as e:
            print(f'Error receiving message: {e}')

    async def __send_periodic(self, interval=2.0):
        try:
            while True:
                data = json.dumps({'latitude': self.latitude, 'longitude': self.longitude})
                await self.__send(data)
                await asyncio.sleep(interval)
        except asyncio.CancelledError:
            print('Periodic sending stopped.')

    async def run(self):
        """Start the drone: connect, send data periodically, and listen for incoming messages."""
        await self.__connect(self.uri)
        if self.websocket:
            try:
                send_task = asyncio.create_task(self.__send_periodic(SEND_INTERVAL))
                receive_task = asyncio.create_task(self.__receive())
                await asyncio.gather(send_task, receive_task)
            except asyncio.CancelledError:
                print('Drone tasks stopped.')
            finally:
                await self.disconnect()

    async def disconnect(self):
        if self.websocket:
            await self.websocket.close()
            print(f'Drone {self.id} disconnected.')


async def simulate_drone(drone_id):
    drone = Drone(drone_id)
    await drone.run()
