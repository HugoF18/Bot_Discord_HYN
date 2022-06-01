
import discord
from discord.ext import commands
intents = discord.Intents.default()
intents.typing = True
intents.members = True

client = commands.Bot(command_prefix = "$", intents = intents)
client.delete_messages = {}

@client.event
async def on_message_delete(message):
    client.delete_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)

@client.command()
async def delete(ctx):
    try:
        contents, author, channel_name, time = client.delete_messages[ctx.guild.id]
        
    except:
        await ctx.channel.send("Aucun message supprimé de trouvé !")
        return

    embed = discord.Embed(description=contents, color=discord.Color.purple(), timestamp=time)
    embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
    embed.set_footer(text=f"sup dans : #{channel_name}")

    await ctx.channel.send(embed=embed)

client.run("ODg5NTcyMTgwMDc2MTUwODA0.G8Vk2R.htMFKVYhFKpykSg3K5jvdTXGc7yryhrDRImShI")



