import asyncio
import os

from dotenv import load_dotenv

from src.bot.Drone import simulate_drone


def main():
    drone_id = os.getenv('DRONE_ID')
    asyncio.run(simulate_drone(drone_id))

if __name__ == '__main__':
    load_dotenv()
    main()