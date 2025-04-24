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

message_map = {}

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id == SALON_SOURCE_ID:
        salon_cible = bot.get_channel(SALON_CIBLE_ID)

        contenu = f"**{message.author.display_name}** : {message.content}"
        fichiers = [await f.to_file() for f in message.attachments]

        msg_envoye = await salon_cible.send(content=contenu, files=fichiers)

        # On enregistre les ID des messages
        message_map[message.id] = msg_envoye.id

@bot.event
async def on_message_delete(message):
    if message.channel.id == SALON_SOURCE_ID and message.id in message_map:
        salon_cible = bot.get_channel(SALON_CIBLE_ID)
        id_message_cible = message_map[message.id]

        try:
            msg_a_supprimer = await salon_cible.fetch_message(id_message_cible)
            await msg_a_supprimer.delete()
        except discord.NotFound:
            pass  # Le message a déjà été supprimé

@bot.event
async def on_message_edit(before, after):
    if before.channel.id == SALON_SOURCE_ID and before.id in message_map:
        salon_cible = bot.get_channel(SALON_CIBLE_ID)
        id_message_cible = message_map[before.id]

        contenu = f" **{after.author.display_name}** (édité) : {after.content}"
        fichiers = [await f.to_file() for f in after.attachments]

        try:
            msg_a_modifier = await salon_cible.fetch_message(id_message_cible)
            await msg_a_modifier.edit(content=contenu)
        except discord.NotFound:
            pass  # Si le message n'existe plus


        """Inversemment"""
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id == SALON_CIBLE_ID:
        salon_source = bot.get_channel(SALON_SOURCE_ID)

        contenu = f"**{message.author.display_name}** : {message.content}"
        fichiers = [await f.to_file() for f in message.attachments]

        msg_envoye = await salon_source.send(content=contenu, files=fichiers)

        # On enregistre les ID des messages
        message_map[message.id] = msg_envoye.id

@bot.event
async def on_message_delete(message):
    if message.channel.id == SALON_CIBLE_ID and message.id in message_map:
        salon_source = bot.get_channel(SALON_SOURCE_ID)
        id_message_source = message_map[message.id]

        try:
            msg_a_supprimer = await salon_source.fetch_message(id_message_source)
            await msg_a_supprimer.delete()
        except discord.NotFound:
            pass  # Le message a déjà été supprimé

@bot.event
async def on_message_edit(before, after):
    if before.channel.id == SALON_CIBLE_ID and before.id in message_map:
        salon_source = bot.get_channel(SALON_SOURCE_ID)
        id_message_source = message_map[before.id]

        contenu = f" **{after.author.display_name}** (édité) : {after.content}"
        fichiers = [await f.to_file() for f in after.attachments]

        try:
            msg_a_modifier = await salon_source.fetch_message(id_message_source)
            await msg_a_modifier.edit(content=contenu)
        except discord.NotFound:
            pass  # Si le message n'existe plus

# """Méssage de bienvenue et d'au revoir"""
# SALON_ARRIVANT_ID = 1356747693266833630
# @bot.event
# async def on_member_join(member):
#     salon = bot.get_channel(SALON_ARRIVANT_ID)
#     await salon.send(f"👋 Bienvenue {member.mention} sur le serveur !")

# SALON_SORTANT_ID = 1356747731519012925
# @bot.event
# async def on_member_remove(member):
#     salon = bot.get_channel(SALON_SORTANT_ID)
#     await salon.send(f"😢 {member.mention} a quitté le serveur...")


keep_alive()
bot.run(token=token)