from typing import Tuple, Mapping, Callable, Optional, Any
import discord


client = discord.Client()
NodeId = str


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
    'start': Node("Comment puis-je vous aidez ?", {'tutoriel': 'tutoriel', 'musique': 'musique', 'documentation': 'documentation'}),
    'tutoriel': Node("Sur quel langage avez vous besoin d'un tutoriel ?", {'python': 'python', 'javascript': 'javascript', 'php': 'php', 'css': 'css', 'html': 'html', 'sql': 'sql', 
                                                                            'retour': 'start'}),
    'musique': Node("Quel style musical voulez-vous ?", {'rock' : 'rock', 'retour': 'start'}),
    'documentation': Node("Quel document avez vous besoin ?", {'retour': 'start'}),
    'python': Node("Voici un lien pour vous aidez : https://www.youtube.com/watch?v=oUJolR5bX6g", {}, exit=True),
    'javascript': Node("Voici un lien pour vous aidez : https://www.youtube.com/watch?v=QB1DTl7HFnc", {}, exit=True),
    'php': Node("Voici un lien pour vous aidez : https://www.youtube.com/watch?v=FKdctsQ1v7U", {}, exit=True),
    'css': Node("Voici un lien pour vous aidez : https://www.youtube.com/watch?v=_-KEFeWLVtY", {}, exit=True),
    'html': Node("Voici un lien pour vous aidez : https://www.youtube.com/watch?v=-PYadbLX40g", {}, exit=True),
    'sql': Node("Voici un lien pour vous aidez : https://www.youtube.com/watch?v=LT02Qz5btVs", {}, exit=True),
    'rock':Node('rock en cours' ,{}, exit=True)
}

@client.event
async def on_message(msg):
    if msg.content == '$aide':
       try:
           await Dialog(nodes, 'start').evaluate(msg)
       except:
           pass

client.run("OTc4MjI5MjIxOTIxMDE3OTE3.GXxjH9.Y26kAfTXSSAO9RQsDROpPUvydnhX8STBott-x4")