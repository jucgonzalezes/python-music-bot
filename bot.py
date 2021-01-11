import discord
import youtube_dl
from youtube_search import YoutubeSearch as YS


def read_token():
    with open("token.dat", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()

client = discord.Client()


@client.event
async def on_ready():
    print(f'Conectado satisfactoriamente al servidor como {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('>p'):
        voice = message.author.voice
        request = " ".join(message.content.split('>p ')[1:])
        print(request)

        result = YS(request, max_results=1).to_dict()[0]
        url = 'http://www.youtube.com' + result['url_suffix']
        print(url)

        # url = a

        if voice is not None:
            vc = voice.channel
            print(vc.name)
            conn = await vc.connect()
            conn.play(discord.FFmpegPCMAudio('./rsc/cc_song.mp3'))
            await message.channel.send('En linea y funcionando.')
            # player - await
        else:
            await message.channel.send('Conectese a un canal de voz antes de '
                                       'usar el bot.')
            return

client.run(token)
