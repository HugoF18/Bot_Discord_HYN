import discord
import os
import asyncio
import youtube_dl
import time


client = discord.Client()
key = "ODg5NTcyMTgwMDc2MTUwODA0.G8Vk2R.htMFKVYhFKpykSg3K5jvdTXGc7yryhrDRImShI"

voice_clients = {}

yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': "-vn"}


@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")


@client.event
async def on_message(message):
    if message.content.startswith("$play"):

        try:
            voice_client = await message.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client
        except:
            print("error")

        try:
            url = message.content.split()[1]

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            song = data['url']
            player = discord.FFmpegPCMAudio(song, **ffmpeg_options, executable="C:\\ffmpeg\\bin\\ffmpeg.exe")

            voice_clients[message.guild.id].play(player)

        except Exception as err:
            print(err)


    if message.content.startswith("$pause"):
        try:
            voice_clients[message.guild.id].pause()
        except Exception as err:
            print(err)

    if message.content.startswith("$resume"):
        try:
            voice_clients[message.guild.id].resume()
        except Exception as err:
            print(err)

    if message.content.startswith("$stop"):
        try:
            voice_clients[message.guild.id].stop()
            await voice_clients[message.guild.id].disconnect()
        except Exception as err:
            print(err)


client.run(key)