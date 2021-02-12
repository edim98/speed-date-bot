import discord
from game import Game

class Bot:
    def __init__(self, token):
        self.client = discord.Client()
        self.token = token
        self.games_queue = []

        @self.client.event
        async def on_ready():
            print('Logged in as {0.user}'.format(self.client))
    
        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return
            if not self.authorize(message):
                return
            await self.parse(message)

    def run(self):
        self.client.run(self.token)

    def authorize(self, message):
        if "admin" not in [str(role) for role in message.author.roles]:
            print('Refused command from: ' + message.author.name)
            return False
        return True
    
    async def parse(self, message):
        if message.content == '!help':
            await message.channel.send('hElP')
        
        if message.content.startswith('!start'):
            if self.games_queue:
                # await message.channel.send('A game is already running!')
                await message.author.send('A game is already running!')
                return

            # !start <channel_name> <time_limit>
            params = message.content.split()[1:]
            guild = message.guild
            start_channel = None

            if params[0] not in [str(vc) for vc in guild.voice_channels]:
                # await message.channel.send('There is no {} voice channel in the {} server! Please try again...'.format(params[0], str(guild)))
                await message.author.send('There is no {} voice channel in the {} server! Please try again...'.format(params[0], str(guild)))
                return
            else:
                start_channel = [vc for vc in guild.voice_channels if str(vc) == params[0]][0]
            
            try:
                max_room_time = int(params[1])
            except:
                # await message.channel.send('Max room size and max room time need to be integer numbers! Please try again...')
                await message.author.send('Max room size and max room time need to be integer numbers! Please try again...')
                return
            else:
                game = Game(self.client, message.author, start_channel, guild, max_room_time)

                current_voice_states = [channel.voice_states for channel in message.guild.voice_channels if str(channel) == params[0]][0]
                
                for k in current_voice_states.keys():
                    member = await guild.fetch_member(k)
                    game.add_player(member)
                
                self.games_queue.append(game)
                await game.start()
                self.games_queue.pop()






    