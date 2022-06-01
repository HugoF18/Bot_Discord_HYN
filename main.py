import discord
from discord.ext import commands
import music

cogs=[music]

client=commands.Bot(command_prefix='?',intents=discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(client)


client.run("ODg5NTcyMTgwMDc2MTUwODA0.G8Vk2R.htMFKVYhFKpykSg3K5jvdTXGc7yryhrDRImShI")