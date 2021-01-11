import discord
from discord.ext import commands
import youtube_dl
from youtube_search import YoutubeSearch as YS
import os


def read_token():
    with open("token.dat", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()

client = commands.Bot(command_prefix='>')

YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': './audio/%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
        # 'postprocessors': [{
        #   'key': 'FFmpegExtractAudio',
        #   'preferredcodec': 'mp3',
        #   'preferredquality': '192',
        #                    }],
    }


@client.event
async def on_ready():
    print(f'Conectado satisfactoriamente al servidor como {client.user}')


@client.command(pass_context=True, aliases=['p'])
async def play(ctx, *args):
    if ctx.author == client.user:
        return
    request = " ".join([arg for arg in args])
    print(request)

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    result = YS(request, max_results=1).to_dict()[0]
    url = 'http://www.youtube.com' + result['url_suffix']
    print(url)

    voice = ctx.message.author.voice
    print(voice)

    if voice is not None:
        vc = voice.channel
        print(vc.name)

        with youtube_dl.YoutubeDL(YTDL_OPTIONS) as ydl:
            ydl.download([url])
        print('Descargada.')
        conn = await vc.connect()
        for file in os.listdir('./audio/'):
            conn.play(discord.FFmpegPCMAudio(f'./audio/{file}'),
                      after=lambda x: os.remove(f'./audio/{file}'))
    else:
        await ctx.channel.send('Conectese a un canal de voz antes de '
                               'usar el bot.')
        return


client.run(token)
