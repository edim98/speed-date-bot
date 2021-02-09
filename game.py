import time
import itertools

class Game:
    def __init__(self, client, start_channel, guild, time_limit):
        self.client = client
        self.start_channel = start_channel
        self.guild = guild
        self.time_limit = time_limit
        self.players = []
    
    def add_player(self, player):
        self.players.append(player)
    
    def add_multiple(self, player_list):
        self.players.extend(player_list)
    
    def get_players(self):
        return self.players

    async def start_date(self, x, y, vc):
        try: 
            await x.move_to(vc)
            await y.move_to(vc)
        except Exception as e:
            print(e)
            await self.start_channel.send('Internal server error...')
            return

    def all_pairs(self, lst):
        if len(lst) < 2:
            yield []
            return
        a = lst[0]
        for i in range(1, len(lst)):
            pair = (a, lst[i])
            for rest in self.all_pairs(lst[1:i] + lst[i+1:]):
                yield [pair] + rest

    def generate_pairings(self, voice_channels):
        result = []
        k = 0
        for round in self.all_pairs(list(range(len(self.players)))):
            j = 0
            for pair in round:
                result.append(
                    {
                        'round': k,
                        'pairing': (self.players[pair[0]], self.players[pair[1]]),
                        'voice_channel': voice_channels[j]
                    }
                )
                j += 1
        
        return result
        

        

    async def start(self):
        text_channels = []
        voice_channels = []

        for i in range(len(self.players) // 2):
            tc = await self.guild.create_text_channel('speed-date-room-' + str(i))
            text_channels.append(tc)
            
            vc = await self.guild.create_voice_channel('speed-date-room-' + str(i))
            voice_channels.append(vc)
        
        pairings = self.generate_pairings(voice_channels)

        counter = 0
        round_no = 0
        queue = []
        for p in pairings:
            await self.start_date(p['pairing'][0], p['pairing'][1], p['voice_channel'])
            queue.append(p)

            counter += 1

            if counter == 2:
                await self.start_channel.send('Starting round {}!'.format(round_no))
                await self.start_channel.send(
                    ''.join(
                        [
                            'Voice channel: {} - {} & {}\n'.format(
                                q['voice_channel'], q['pairing'][0], q['pairing'][1]
                            ) for q in queue
                        ]
                    )
                )
                time.sleep((self.time_limit - 1) * 60)
                await self.start_channel.send('1 minute remaining until next swap!')
                time.sleep(60)
                counter = 0
                queue = []

        
        
