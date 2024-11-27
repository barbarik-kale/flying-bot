import asyncio
from dotenv import load_dotenv

from src.bot.controller_bot import simulate_controller
from src.bot.drone_bot import simulate_drone
from src.drone.services import DroneService


async def main():
    """
    Fetches list of drones and simulates drone bots and controller bots in async mode
    """
    data, error = DroneService.get_drone_list()
    drone_list = data.get('data')

    tasks = []
    for drone in drone_list:
        tasks.append(simulate_drone(drone.get('id')))
        tasks.append(simulate_controller(drone.get('id')))
        break

    await asyncio.gather(*tasks)

if __name__ == '__main__':
    load_dotenv()
    asyncio.run(main())