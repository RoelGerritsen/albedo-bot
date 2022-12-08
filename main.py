import discord 
from discord import app_commands
from replit import db
import os
from keep_alive import keep_alive
from database import keyInDatabase
from little_ai import communications

role_channel = 1049433665832243200

class reaction_role: 
  role: discord.Role
  emoji: str
  def __init__(self, role: discord.Role, emoji: str):
    self.role = role
    self.emoji = emoji

client = discord.Client(intents=discord.Intents().all())
tree = app_commands.CommandTree(client)
someVar = []

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  await tree.sync()

@tree.command(name='create_reaction_role', description='ADDED WHEN WORKS')
async def create_reaction_role(interaction: discord.Interaction, role: discord.Role, emoji: str):
  someVar.append(reaction_role(role,emoji))
  return await interaction.response.send_message('Succes',ephemeral=True)

@client.event
async def on_raw_reaction_add(payLoad):
  guild = client.get_guild(payLoad.guild_id)
  if payLoad.channel_id == role_channel:
    for var in someVar:
      if  var.emoji.rfind(payLoad.emoji.name) > -1:
        return await payLoad.member.add_roles(guild.get_role(var.role.id))

@client.event
async def on_raw_reaction_remove(payLoad):
  guild = client.get_guild(payLoad.guild_id)
  member = guild.get_member(payLoad.user_id)
  if payLoad.channel_id == role_channel:
    for var in someVar:
      if  var.emoji.rfind(payLoad.emoji.name) > -1:
        return await member.remove_roles(guild.get_role(var.role.id))
      
@client.event
async def on_message(message):
  if message.author == client.user:
    return

keep_alive()
client.run(os.getenv('TOKEN'))