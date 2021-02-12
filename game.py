import time
import itertools

class Game:
    def __init__(self, client, comm_channel, start_channel, guild, time_limit):
        self.client = client
        self.comm_channel = comm_channel
        self.start_channel = start_channel
        self.guild = guild
        self.time_limit = time_limit
        self.players = []
        self.text_channels = []
        self.voice_channels = []
    
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
            await self.comm_channel.send('Internal server error...')
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
            k += 1
        
        return result   

    async def start(self):

        no_rooms = len(self.players) // 2

        for i in range(no_rooms):
            tc = await self.guild.create_text_channel('speed-date-room-' + str(i))
            self.text_channels.append(tc)
            
            vc = await self.guild.create_voice_channel('speed-date-room-' + str(i))
            self.voice_channels.append(vc)
        
        pairings = self.generate_pairings(self.voice_channels)

        counter = 0
        round_no = 1
        queue = []
        for p in pairings:
            await self.start_date(p['pairing'][0], p['pairing'][1], p['voice_channel'])
            queue.append(p)

            counter += 1

            if counter == no_rooms:
                await self.comm_channel.send('Starting round {}!'.format(round_no))
                await self.comm_channel.send(
                    ''.join(
                        [
                            'Voice channel: {} - {} & {}\n'.format(
                                q['voice_channel'], q['pairing'][0], q['pairing'][1]
                            ) for q in queue
                        ]
                    )
                )

                time.sleep((self.time_limit - 1) * 60)

                await self.send_to_all(60)
                time.sleep(30)
                await self.send_to_all(30)
                time.sleep(20)
                await self.send_to_all(10)
                time.sleep(10)

                counter = 0
                queue = []
                round_no += 1
        
        await self.comm_channel.send('Speed date event is now over! You will be returned to the original voice channel in a couple of seconds... Thank you for participating :)')
        time.sleep(5)
        await self.clear_and_exit()
        return

        
    async def clear_and_exit(self):
        for player in self.players:
            try:
                await player.move_to(self.start_channel)
            except Exception as e:
                print(e)
                await self.comm_channel.send('Internal server error...')
        
        for tc in self.text_channels:
            try:
                await tc.delete()
            except Exception as e:
                print(e)
        
        for vc in self.voice_channels:
            try:
                await vc.delete()
            except Exception as e:
                print(e)

    async def send_to_all(self, timer):
        await self.comm_channel.send('{} seconds remaining until next round!'.format(timer))
        for tc in self.text_channels:
            tc.send('{} seconds remaining until next round!'.format(timer))