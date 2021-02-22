import time
import asyncio

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
        self.pause_flag = False
    
    async def set_pause(self):
        if self.pause_flag:
            await self.comm_channel.send('Game was unpaused!')
        else:
            await self.comm_channel.send('Game was paused!')
        self.pause_flag = not self.pause_flag
    
    def add_player(self, player):
        self.players.append(player)
    
    def add_multiple(self, player_list):
        self.players.extend(player_list)
    
    def get_players(self):
        return self.players
    
    async def pause(self):
        while self.pause_flag:
            await asyncio.sleep(0.25)
        return

    async def start_date(self, x, y, vc):
        try: 
            await x.move_to(vc)
        except Exception as e:
            print(e)
            await self.comm_channel.send('Internal server error...')

        try:
            await y.move_to(vc)
        except Exception as e:
            print(e)
            await self.comm_channel.send('Internal server error...')

    def all_pairs(self, lst): 
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
                            'Voice channel: {} - {}\t&\t{}\n'.format(
                                q['voice_channel'], q['pairing'][0], q['pairing'][1]
                            ) for q in queue
                        ]
                    )
                )

                await self.wait_until((self.time_limit - 1) * 60)

                await self.send_to_all(60, round_no)

                await self.wait_until(30)

                await self.send_to_all(30, round_no)

                await self.wait_until(20)

                await self.send_to_all(10, round_no)

                await self.wait_until(10)

                counter = 0
                queue = []
                round_no += 1
        
        await self.clear_and_exit()
        return

        
    async def clear_and_exit(self):
        for tc in self.text_channels:
            await tc.send('Speed date event is now over! You will be returned to the original voice channel in a couple of seconds... Thank you for participating :)')
        await asyncio.sleep(5)

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

    async def send_to_all(self, timer, round_no):
        await self.comm_channel.send('{} seconds remaining until round {}!'.format(timer, round_no))
        for tc in self.text_channels:
            await tc.send('{} seconds remaining until round {}!'.format(timer, round_no))

    async def wait_until(self, timeout, period=0.25):
        must_end = time.time() + timeout
        while time.time() < must_end:
            if self.pause_flag:
                still_to_wait = must_end - time.time()
                await self.pause()
                must_end = time.time() + still_to_wait
            await asyncio.sleep(period)