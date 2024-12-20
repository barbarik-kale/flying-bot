import asyncio
import json
import os
import random

import websockets

from src.drone.services import DroneService
from src.ws.services import TokenService

CONTROLLER_SEND_INTERVAL = 1.0

class Controller:
    def __init__(self, drone_id):
        """
        initialize drone details, token and websocket uri
        """
        details, error = DroneService.get_drone(drone_id)
        details = details.get('data')
        self.id = drone_id
        self.name = details.get('name')
        self.avg_speed_ms = details.get('avg_speed_ms')
        self.token = os.getenv('AUTH_TOKEN')
        self.ws_uri = os.getenv('CONTROLLER_WS_URI')
        self.latitude = 0
        self.longitude = 0
        self.websocket = None

    def __handle_message(self, message):
        try:
            print(f'Message length = {len(message)}')
            print(f'Message length = {message}')
            message = json.loads(message)
            self.latitude = message.get('latitude', self.latitude)
            self.longitude = message.get('longitude', self.longitude)
        except Exception as e:
            pass

    async def __connect(self):
        ws_token = TokenService.get_ws_token(self.id)
        uri = f'{self.ws_uri}?token={ws_token}'
        try:
            self.websocket = await websockets.connect(uri)
            print(f'Controller {self.id} connected to {uri}')
        except Exception as e:
            print(f'Error connecting drone {self.id}: {e}')

    async def __receive_data(self):
        try:
            async for message in self.websocket:
                self.__handle_message(message)
        except Exception as e:
            print(f'Error receiving message: {e}')

    async def __send_data(self, data):
        if self.websocket:
            try:
                await self.websocket.send(data)
            except Exception as e:
                print(f'Error sending data: {e}')
        else:
            print('Not connected to the server.')

    async def __send_periodic(self, interval=5.0):
        try:
            while True:
                commands = ['LEFT', 'RIGHT', 'UP', 'DOWN']
                choice = random.choice(commands)
                data = '{"command":"' + choice + '"}'
                await self.__send_data(data)
                await asyncio.sleep(interval)
        except asyncio.CancelledError:
            print('Periodic sending stopped.')

    async def run(self):
        await self.__connect()
        send_task = asyncio.create_task(self.__send_periodic(CONTROLLER_SEND_INTERVAL))
        recv_task = asyncio.create_task(self.__receive_data())
        await asyncio.gather(send_task, recv_task)

async def simulate_controller(drone_id):
    controller = Controller(drone_id)
    await controller.run()