from dotenv import load_dotenv
import os
from bot import Bot
import discord

load_dotenv()
CLIENT_TOKEN = os.getenv('TEST_TOKEN_3')

def main():
    client = discord.Client()

    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        if message.content == '!connect':
            vc = message.content.split()[1:]

            await message.author.voice.channel.connect()
            for voice in client.voice_clients:
                voice.stop()

        if message.content == '!stop':
            for voice in client.voice_clients:
                voice.stop()
                await voice.disconnect()
            await client.close()

    client.run(CLIENT_TOKEN)

if __name__ == "__main__":
    main()
