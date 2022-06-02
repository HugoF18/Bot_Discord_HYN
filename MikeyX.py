import discord
import random
from typing import Tuple, Mapping, Callable, Optional, Any
from discord.ext import commands
import asyncio
import youtube_dl
intents = discord.Intents.default()
intents.typing = True
intents.members = True

NodeId = str

client = commands.Bot(command_prefix = "$", intents = intents, help_command=None)
client.delete_messages = {}
voice_clients = {}

yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': "-vn"}


dico_flag = {1: {'france': ':flag_fr:'}, 
            2 : {'cambodge': ':flag_kh:'},
            3 : {'pologne': ':flag_pl:'},
            4 : {'italie': ':flag_it:'},
            5 : {'japon': ':flag_jp:'},
            6 : {'vietnam': ':flag_vn:'},
            7 : {'seychelles': ':flag_sc:'},
            8 : {'bosnie herzégovine': ':flag_ba:'},
            9 : {'madagascar': ':flag_mg:'},
            10 : {'corée du sud': ':flag_kr:'}

}
dico_hiragana =  {1: {'a': 'あ'}, 
            2 : {'i': 'い'},
            3 : {'u': 'う'},
            4 : {'e': 'え'},
            5 : {'o': 'お'},
            6 : {'ka': 'か'},
            7 : {'ki': 'き'},
            8 : {'ku': 'く'},
            9 : {'ke': 'け'},
            10 : {'ko': 'こ'},
            11 : {'sa': 'さ'},            
            12 : {'shi': 'し'},
            13 : {'su': 'す'},
            14 : {'se': 'せ'},
            15 : {'so': 'そ'},
            16 : {'ta': 'た'},
            17 : {'chi': 'ち'},
            18 : {'tsu': 'つ'},
            19 : {'te': 'て'},
            20 : {'to': 'と'},
            21 : {'na': 'な'},
            22 : {'ni': 'に'},
            23 : {'nu': 'ぬ'},
            24 : {'ne': 'ね'},
            25 : {'no': 'の'},
            26 : {'ha': 'は'},
            27 : {'hi': 'ひ'},
            28 : {'fu': 'ふ'},
            29 : {'he': 'へ'},
            30 : {'ho': 'ほ'},
            31:  {'ma': 'ま'},
            32 : {'mi': 'み'},
            33 : {'mu': 'む'},
            34 : {'me': 'め'},
            35 : {'mo': 'も'},
            36 : {'ra': 'ら'},
            37 : {'ri': 'り'},
            38 : {'ru': 'る'},
            39 : {'re': 'れ'},
            40 : {'wa': 'わ'},
            41 : {'wo': 'を'},
            42 : {'ya': 'や'},
            43 : {'yu': 'ゆ'},
            44 : {'yo': 'よ'},
            45 : {'n': 'ん'}
}

class Node:

    def __init__(self,
                 text_on_enter: Optional[str],
                 choices: Mapping[str, Tuple[NodeId, Callable[[Any], None]]],
                 exit: bool = False):
        self.text_on_enter = text_on_enter
        self.choices = choices
        self.exit = exit

    async def walk_from(self, message) -> Optional[NodeId]:

        if self.text_on_enter:
            await message.channel.send(self.text_on_enter)

        if self.exit: 
            return None

        def is_my_message(msg):
            return msg.author == message.author and msg.channel == message.channel
        user_message = await client.wait_for("message", check=is_my_message)
        choice = user_message.content
        while choice not in self.choices:
            await message.channel.send("Voici ce qui est possible : " + ', '.join(list(self.choices)))       
            user_message = await client.wait_for("message", check=is_my_message)
            choice = user_message.content

        result = self.choices[choice]
        if isinstance(result, tuple):
            next_id, mod_func = self.choices[choice]
            mod_func(self)
        else: next_id = result
        return next_id

class Dialog:

    def __init__(self, nodes={}, entry_node=None):
        self.nodes: Mapping[NodeId, Node] = nodes
        self.entry_node: NodeId = entry_node

    def add_node(self, id: NodeId, node: Node):

        self.nodes[id] = node

    def set_entry(self, id: NodeId):

        self.entry_node = id

    async def evaluate(self, message):

        current_node = self.nodes[self.entry_node]
        while current_node is not None:
            next_node_id = await current_node.walk_from(message)
            if next_node_id is None: 
                return
            current_node = self.nodes[next_node_id]

nodes = {
    'start': Node("Comment puis-je vous aidez ?", {'tutoriel': 'tutoriel', 'musique': 'musique', 'langue': 'langue', 'exit' : 'exit'}),
    'tutoriel': Node("Sur quel langage avez vous besoin d'un tutoriel ?", {'python': 'python', 'javascript': 'javascript', 'php': 'php', 'css': 'css', 'html': 'html', 'sql': 'sql', 
                                                                            'retour': 'start','exit' : 'exit' }),
    'musique': Node("Quel style musical voulez-vous ?", {'rock' : 'rock', 'pop': 'pop','op anime' : 'op anime', 'metal' : 'metal', 'retour': 'start','exit' : 'exit'}),
    'langue': Node("Quel langue avez vous besoin ?", {'japonais': 'japonais','polonais': 'polonais','retour': 'start','exit' : 'exit'}),
    'japonais' : Node("Quelle niveau avait vous ? ", {'facile' : 'facile_jp','moyen' : 'moyen_jp','difficile' : 'difficile_jp','retour':'start','exit' : 'exit'}),
    'polonais' : Node("Quelle niveau avait vous ? ", {'facile' : 'facile_pl','moyen' : 'moyen_pl','difficile' : 'difficile_pl','retour':'start','exit' : 'exit'}),
    'python': Node("Voici un lien pour vous aidez : https://www.youtube.com/watch?v=oUJolR5bX6g", {}, exit=True),
    'javascript': Node("Voici un lien pour vous aidez : https://www.youtube.com/watch?v=QB1DTl7HFnc", {}, exit=True),
    'php': Node("Voici un lien pour vous aidez : https://www.youtube.com/watch?v=FKdctsQ1v7U", {}, exit=True),
    'css': Node("Voici un lien pour vous aidez : https://www.youtube.com/watch?v=_-KEFeWLVtY", {}, exit=True),
    'html': Node("Voici un lien pour vous aidez : https://www.youtube.com/watch?v=-PYadbLX40g", {}, exit=True),
    'sql': Node("Voici un lien pour vous aidez : https://www.youtube.com/watch?v=LT02Qz5btVs", {}, exit=True),
    'rock':Node("Voici une musique qui pourrait vous plaire : https://www.youtube.com/watch?v=-tJYN-eG1zk" ,{}, exit=True),
    'pop' : Node("Voici une musique qui pourrait vous plaire : https://www.youtube.com/watch?v=QNJL6nfu__Q" ,{}, exit=True),
    'op anime' : Node("Voici une musique qui pourrait vous plaire : https://www.youtube.com/watch?v=fodAJ-1dN3I" ,{}, exit=True),
    'metal' : Node("Voici une musique qui pourrait vous plaire : https://www.youtube.com/watch?v=tAGnKpE4NCI" ,{}, exit=True),
    'exit' : Node("J'espère que je vous ai bien aidé." ,{}, exit=True),
    'facile_jp' : Node("Voici une vidéo pour commencer : https://www.youtube.com/watch?v=Hs8oR3xDokA" ,{}, exit=True),
    'moyen_jp' : Node("Voici une vidéo pour vous améliorer : https://www.youtube.com/watch?v=dW27PVKF92Y" ,{}, exit=True),
    'difficile_jp' : Node("Voici une vidéo pour vous expertiser :https://www.youtube.com/watch?v=yhsDvEfKqoQ" ,{}, exit=True),
    'facile_pl' : Node("Voici une vidéo pour commencer : https://www.youtube.com/watch?v=gjzMH7XTmg8" ,{}, exit=True),
    'moyen_pl' : Node("Voici une vidéo pour vous améliorer : https://www.youtube.com/watch?v=--vWDl-JaKU" ,{}, exit=True),
    'difficile_pl' : Node("Voici une vidéo pour vous expertiser : https://www.youtube.com/watch?v=EzccZqPZ9Tk" ,{}, exit=True),
}

@client.event
async def on_message(message):
    
    Help_channel = client.get_channel(978634583346130944)
    if message.author == client.user:
        return
    if message.channel == Help_channel and message.content.startswith('$commande'):
        await Help_channel.send('`$flag = jeux des drapeaux / $hira = deviner les hiragana / $admin = ping admin / $help = trouve ce que tu veux / $delete = reprends le dernier message supprimé / $play = joue de la musique (lien youtube)`')

    def author_check(author):
        return lambda message: message.author == author
    

    if message.content.startswith("$play"):

        try:
            voice_client = await message.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client
        except:
            print("error")

        try:
            
            url = message.content.split()[1]
            print(url)
            
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
    
    message.content = message.content.lower()
    if message.channel == Help_channel and message.content.startswith('$flag'):
        score = 0
        round = 0
        while round !=3:
            await Help_channel.send('Quel est ce pays ?')
            aléa = random.randint(1,10)
            dico_flag_value = dico_flag[aléa]
            for key in dico_flag_value.values():
                await Help_channel.send(key)
                country = random.choice(list(dico_flag[aléa]))
                message = await client.wait_for("message", check=author_check(message.author), timeout=30.0)
                if message.content == country:
                    await Help_channel.send('bien joué')
                    score +=1
                    round +=1
                else:
                    await Help_channel.send('Raté')
                    round+=1
        score_str = str(score)
        await Help_channel.send('Score = ' + score_str + '/3')


    if message.channel == Help_channel and message.content.startswith('$hira'):
        score = 0
        round = 0
        while round != 3 :
            aléa = random.randint(1,45)
            dico_hiragana_value = dico_hiragana[aléa]
            for key in dico_hiragana_value.values():
                await Help_channel.send(key)
                hira = random.choice(list(dico_hiragana[aléa]))
                message = await client.wait_for("message", check=author_check(message.author), timeout=30.0)
                if message.content == hira:
                    await Help_channel.send('bien joué')
                    score = score + 1
                    round = round + 1
                else:
                    await Help_channel.send('Raté') 
                    round = round + 1
        score_str = str(score)
        await Help_channel.send('Score = ' + score_str + '/3')
    
    if message.content == '$help':
       try:
           await Dialog(nodes, 'start').evaluate(message)
       except:
           pass

    if message.channel == Help_channel and message.content.startswith('$admin'):
        await Help_channel.send("Bonjour <@&978639487498321971> quelqu'un a besoin d'aide")

    
    
    await client.process_commands(message)

@client.event
async def on_member_join(member):
    Help_channel = client.get_channel(978634583346130944)
    guild = client.get_guild(978634543152136193)
    #Welcome Members
    await Help_channel.send(f'Bienvenue {member.mention}!')
    # Welcome DM Members
    await member.send(f'Bienvenue {member.name} sur le serveur {guild.name} où nous faisons nos test :face_with_hand_over_mouth:')


@client.event
async def on_message_delete(msg):
    client.delete_messages[msg.guild.id] = (msg.content, msg.author, msg.channel.name, msg.created_at)
    
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
