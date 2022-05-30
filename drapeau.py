import discord
import random
from random import choices

client = discord.Client()

dico_flag = {1: {'France': ':flag_fr:'}, 
            2 : {'Cambodge': ':flag_kh:'},
            3 : {'Pologne': ':flag_pl:'}
}

@client.event
async def on_message(message):
    
    Help_channel = client.get_channel(978233339024637972)
    if message.author == client.user:
        return

    def author_check(author):
        return lambda message: message.author == author
    
    if message.channel == Help_channel and message.content.startswith('$flag'):
        await Help_channel.send('Attention majuscule aux pays')
        aléa = random.randint(1,3)
        dico_flag_value = dico_flag[aléa]
        for key in dico_flag_value.values():
            await Help_channel.send(key)
            country = random.choice(list(dico_flag[aléa]))
            message = await client.wait_for("message", check=author_check(message.author), timeout=30.0)
            if message.content == country:
                await Help_channel.send('bien joué')
            else:
                await Help_channel.send('Raté')


client.run("OTc4MjI5MjIxOTIxMDE3OTE3.GXxjH9.Y26kAfTXSSAO9RQsDROpPUvydnhX8STBott-x4")