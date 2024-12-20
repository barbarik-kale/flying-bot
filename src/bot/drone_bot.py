import asyncio
import json
import os

import cv2
import websockets

from src.drone.services import DroneService
from src.ws.services import TokenService

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
        ws_token = TokenService.get_ws_token(self.id)
        uri = f'{uri}?token={ws_token}'
        try:
            self.websocket = await websockets.connect(uri)
            print(f'Drone {self.id} connected to {uri}')
        except Exception as e:
            print(f'Error connecting drone {self.id}: {e}')

    async  def __send_media(self, bytes_data):
        if self.websocket:
            try:
                await self.websocket.send(bytes_data)
            except Exception as e:
                print(f'Error sending data: {e}')
        else:
            print('Not connected to the server.')

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

    async def __video_send_task(self):
        file_path = os.getenv('FILE_PATH')
        video = cv2.VideoCapture(file_path)

        if not video.isOpened():
            print(f'Failed to open video {file_path}')

        while True:
            ret, frame = video.read()
            if not ret:
                video = cv2.VideoCapture(file_path)

            _, buffer = cv2.imencode('.jpg', frame)

            await self.__send_media(buffer.tobytes())
            print('media sent')
            await asyncio.sleep(3)

    async def run(self):
        """Start the drone: connect, send data periodically, and listen for incoming messages."""
        await self.__connect(self.uri)
        if self.websocket:
            try:
                send_task = asyncio.create_task(self.__send_periodic(SEND_INTERVAL))
                receive_task = asyncio.create_task(self.__receive())
                video_task = asyncio.create_task(self.__video_send_task())
                await asyncio.gather(send_task, receive_task, video_task)
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
