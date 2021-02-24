from dotenv import load_dotenv
import os
from bot import Bot
import asyncio

load_dotenv()
CLIENT_TOKEN = os.getenv('TOKEN')

def main():
    b = Bot(CLIENT_TOKEN)
    b.run()

if __name__ == "__main__":
    main()
