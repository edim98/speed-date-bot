#76816 - permissions

import discord
from dotenv import load_dotenv
import os

load_dotenv()
CLIENT_TOKEN = os.getenv("TOKEN")

client = discord.Client()

async def pair(x, y, vc):
    # Pair user x and y in the vc voice channel
    try:
        await x.move_to(vc)
        await y.move_to(vc)
    except e:
        print(e)
        await message.channel.send('Internal server error...')
        return

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "admin" not in [str(role) for role in message.author.roles]:
        print('Refused command from: ' + message.author.name)
        return

    if message.content == "!help":
        print('haha')
        await message.channel.send('hElP')

    if message.content.startswith("!start"):
        # !start <channel name> <time_per_room>
        params = message.content.split()[1:]
        guild = message.guild

        if params[0] not in [str(vc) for vc in guild.voice_channels]:
            await message.channel.send('There is no {} voice channel in the {} server! Please try again...'.format(params[0], str(guild)))
            return

        try:
            max_room_time = int(params[1])
        except e:
            print(e)
            await message.channel.send('Max room size and max room time need to be integer numbers! Please try again...')
            return
        else:
            current_voice_states = [channel.voice_states for channel in message.guild.voice_channels if str(channel) == params[0]][0]

            members_list = []

            for k in current_voice_states.keys():
                member = await guild.fetch_member(k)
                members_list.append(member)

            if len(members_list) % 2:
                await message.channel.send('Number of participants must be even! Please try again...')
                return

            no_pairings = len(members_list) / 2

            text_channels = []
            voice_channels = []
            for i in range(no_pairings):
                tc = await guild.create_text_channel('speed-date-room-' + str(i))
                text_channels.append(tc)

                vc = await guild.create_voice_channel('speed-date-room-' + str(i))
                voice_channels.append(vc)

            for i in range(1, len(members_list)):
                cursor = 0
                for j in range(no_pairings):
                    await pair(members_list[cursor], members_list[(cursor + 1) % n], j)
                    cursor = (cursor + i) % n
                    time.sleep((max_room_time - 1) * 60)
                    await message.channel.send('1 minute remaining!')
                    time.sleep(60)


client.run(CLIENT_TOKEN)
