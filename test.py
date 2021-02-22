from dotenv import load_dotenv
import os
from bot import Bot
import discord

load_dotenv()
CLIENT_TOKEN = os.getenv('TEST_TOKEN_2')

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

def all_pairs(lst): 
    pairings = []
    n = len(lst)
    labels = {
        "inf": lst[0]
    }
    for i in range(n - 1):
        labels[i] = lst[i + 1]
        pairings.append([])

    for i in range(n - 1):
        pairings[i].append((labels['inf'], labels[i]))
        for k in range(1, n//2):
            pairings[i].append((labels[(i + k) % (n - 1)], labels[(i - k) % (n - 1)]))
    return pairings


if __name__ == "__main__":
    # main()
    x = all_pairs([1,2,3,4, 5, 6, 7, 8, 9, 10])
    print(x)
    print(len(x) == 9)
