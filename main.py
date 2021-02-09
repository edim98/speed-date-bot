from dotenv import load_dotenv
import os
from bot import Bot

load_dotenv()
CLIENT_TOKEN = os.getenv('TOKEN')

def main():
    b = Bot(CLIENT_TOKEN)
    b.run()
    print('sal')

if __name__ == "__main__":
    main()
