# import discord
# client =  discord.Client()

# @client.event
# async def on_message(message):
#     user_id = message.author.id
#     message.content = message.content.lower()

#     if message.author == client.user:
#         return
        
#     Help_channel = client.get_channel(978270879010160651)


#     if message.channel == Help_channel and message.content.startswith('$h'):
#         await Help_channel.send('Bonjour !'+str(user_id))
    
#     if message.channel == Help_channel and message.content.startswith('$od'):
#         await Help_channel.send('ok dac')

#     if message.content == "del":
#         await message.channel.purge(limit=3)

# client.run("ODg5NTcyMTgwMDc2MTUwODA0.G8Vk2R.htMFKVYhFKpykSg3K5jvdTXGc7yryhrDRImShI")