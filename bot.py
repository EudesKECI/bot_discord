import os
from dotenv import load_dotenv
import discord
from keep_alive import keep_alive

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = discord.Client(intents = discord.Intents.all())

# À personnaliser
SALON_SOURCE_ID = 1356746947008139415  # ID du salon sur le serveur A
SALON_CIBLE_ID = 1364577267312754769  # ID du salon sur le serveur B

@bot.event
async def on_ready():
    print(f"===== Bot connecté en tant que {bot.user} =====")



@bot.event
async def on_message(message):
    """fonction permettant de partager les messages d'un salon d'un serveur 
    vers un salon d'un autre serveur """
    if message.author.bot:
        return

    if message.channel.id == SALON_SOURCE_ID:
        salon_cible = bot.get_channel(SALON_CIBLE_ID)

        # Contenu du message
        contenu = f"**{message.author.display_name}** : {message.content}"
        fichiers = []

        # Traiter les pièces jointes (images, fichiers, etc.)
        for piece in message.attachments:
            fichiers.append(await piece.to_file())

        await salon_cible.send(content=contenu, files=fichiers)
    
        #inversement

    if message.channel.id == SALON_CIBLE_ID:
        salon_source = bot.get_channel(SALON_SOURCE_ID)

        # Contenu du message
        contenu = f"**{message.author.display_name}** : {message.content}"
        fichiers = []

        # Traiter les pièces jointes (images, fichiers, etc.)
        for piece in message.attachments:
            fichiers.append(await piece.to_file())

        await salon_source.send(content=contenu, files=fichiers)


SALON_ARRIVANT_ID = 1356747693266833630
@bot.event
async def on_member_join(member):
    salon = bot.get_channel(SALON_ARRIVANT_ID)
    await salon.send(f"👋 Bienvenue {member.mention} sur le serveur !")

SALON_SORTANT_ID = 1356747731519012925
@bot.event
async def on_member_remove(member):
    salon = bot.get_channel(SALON_SORTANT_ID)
    await salon.send(f"😢 {member.mention} a quitté le serveur...")


keep_alive()
bot.run(token=token)