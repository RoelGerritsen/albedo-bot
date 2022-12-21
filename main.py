import discord
import aiosqlite
from discord import app_commands

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
    print("Albedos ready to go")
    async with aiosqlite.connect("players.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER, uid INTEGER)')
        await db.commit()

# REACTION ROLE METHODS


@tree.command(name='create_reaction_role', description='ADDS AN REACTION ROLE')
async def create_reaction_role(interaction: discord.Interaction, role: discord.Role, emoji: str):
    someVar.append(reaction_role(role, emoji))
    return await interaction.response.send_message('Succes', ephemeral=True)


@client.event
async def on_raw_reaction_add(payLoad):
    guild = client.get_guild(payLoad.guild_id)
    if payLoad.channel_id == role_channel:
        for var in someVar:
            if var.emoji.rfind(payLoad.emoji.name) > - 1:
                return await payLoad.member.add_roles(guild.get_role(var.role.id))


@client.event
async def on_raw_reaction_remove(payLoad):
    guild = client.get_guild(payLoad.guild_id)
    member = guild.get_member(payLoad.user_id)
    if payLoad.channel_id == role_channel:
        for var in someVar:
            if var.emoji.rfind(payLoad.emoji.name) > -1:
                return await member.remove_roles(guild.get_role(var.role.id))


# UID SAVE METHODS

@tree.command(name="save-uid", description="To save your UID in my database")
async def save_uid(interaction: discord.Interaction, uid: int):
    userId = interaction.user.id
    print(uid)
    async with aiosqlite.connect("players.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('SELECT uid FROM users WHERE id = ?', (userId,))
            data = await cursor.fetchone()
            if data:
                await cursor.execute('UPDATE users SET uid = ? WHERE id = ?', (uid, userId))
            else:
                await cursor.execute('INSERT INTO users VALUES (?,?)', (userId, uid))
        await db.commit()
    return await interaction.response.send_message('Saved your UID', ephemeral=True)


@tree.command(name="get-uid", description="To get someones uid")
async def get_uid(interaction: discord.Interaction, user: discord.User):
    await interaction.response.defer(ephemeral=True)
    userId = user.id
    async with aiosqlite.connect("players.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('SELECT uid FROM users WHERE id = ?', (userId,))
            uid = await cursor.fetchone()
            if uid:
                return await interaction.followup.send(uid[0])
            else:
                return await interaction.followup.send('CANT FIND YOUR SHIT')

# RESPONSE METHODS


@client.event
async def on_message(message):
    msg = message.content
    if message.author == client.user:
        return
    if message.content.startswith('Albedo'):
        if msg.rfind('pog') > -1:
            return await message.channel.send('POGGG')
    if message.content.startswith('Hello'):
        return await message.channel.send('Hello')

    if msg.rfind('Linnea') > -1:
        if msg.rfind('dumb') > -1:
            return await message.channel.send('TRUEEE')

client.run(
    'MTA0OTA2NjAyNDI2NTMzMDc4OA.GnDC-U.dvqXq2kdlHSdXlr50W3Uekw91IqcgIBqldPceo')
