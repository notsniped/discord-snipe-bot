# Imports
import os
import time
import os.path
import discord
import json
import framework.auth
import framework.logger
from datetime import datetime
from discord import ApplicationContext, option
from discord.ext import commands
from discord.ext.commands import *

# Variables
auth = framework.auth.Auth()
botVer = 'v1.2.1'
if os.name == 'nt': os.system('cls')
else: os.system('clear')
intents = discord.Intents.default()
intents.message_content = (True)
client = discord.Bot(intents=intents)
global startTime
startTime = time.time()
config = auth.get_raw()

# Pre-Initialization Commands
def create_files():
    """Creates new database/log files for the client, if they are missing from the bot directory."""
    # Create any missing log files
    if not os.path.isdir("logs"):
        os.mkdir("logs")
        open("logs/snipe.log", 'x', encoding="utf-8")
        open("logs/editsnipe.log", 'x', encoding="utf-8")
        open("logs/errors.log", 'x', encoding="utf-8")
    
    # Create database files
    databases = ["snipe.json", "editsnipe.json"]
    for db in databases:
        if not os.path.isfile(db):
            print(f"[!] \"{db}\" appears to be missing from directory. Creating file...")
            with open(db, 'x', encoding="utf-8") as f:
                json.dump({}, f)
                f.close()

create_files()
auth.initial_setup()  # Check if bot token and owner username are missing and ask user if they want to add it

owner = auth.get_owner_name()

snipe_log: bool = config[str("config")][str("logs")]["snipe"]
editsnipe_log: bool = config[str("config")][str("logs")]["editsnipe"]

logger = framework.logger.Logger()

# Initialize dicts for snipe and editsnipe data
with open("snipe.json", 'r', encoding="utf-8") as f:
    snipe_data: dict = json.load(f)

with open("editsnipe.json", 'r', encoding="utf-8") as f:
    editsnipe_data: dict = json.load(f)

def save():
    """Dumps the latest cached data of the databases to local storage."""
    with open("snipe.json", 'w+', encoding="utf-8") as f:
        json.dump(snipe_data, f, indent=4)

    with open("editsnipe.json", 'w+', encoding="utf-8") as f:
        json.dump(editsnipe_data, f, indent=4)

def generate_data_entries(guild_id: int) -> int:
    if str(guild_id) not in snipe_data:
        snipe_data[str(guild_id)] = {}
    save()

# API Events
@client.event
async def on_ready():
    print(f'Logged on to Discord as {client.user.name}')
    print('====================')
    print('Some client info:')
    print('------------------')
    print(f'  Latency: {round(client.latency * 1000)}ms')
    print(f'  Startup time: {round(startTime)}')
    print(f'  Owner: {str(owner)}')
    print('------------------')
    print('====================')

@client.event
async def on_message(ctx):
    with open("database.json", 'r', encoding="utf-8") as f: data = json.load(f)
    if str(ctx.guild.id) not in data["audit_channel"]:
        data["audit_channel"][str(ctx.guild.id)] = None
    with open("database.json", 'w+', encoding="utf-8") as f: json.dump(data, f, indent=4)

    generate_data_entries(ctx.guild.id)

@client.event
async def on_message_delete(message):
    if not message.author.bot:
        generate_data_entries(message.guild.id)

        dts = time.time()

        # Perform formatting for new Discord usernames.
        author_name: str = message.author.name
        author_name_split = author_name.split("#")
        if author_name_split[-1] == 0:
            author_name = author_name_split[0]

        # Save the deleted message content to database
        snipe_data[str(message.guild.id)][str(message.channel.id)]["latest"] = {
            "content": message.content,
            "author_name": author_name,
            "time_stamp": str(round(dts))
        }
        snipe_data[str(message.guild.id)][str(message.channel.id)][str(message.author.id)] = {
            "content": message.content,
            "author_name": author_name,
            "time_stamp": str(round(dts))
        }

        # Log the edited message content to the client deleted message log.
        if bool(snipe_log):
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"[{timestamp}] Message deleted in #{message.channel} ({message.guild}):\n   Message content: {message.content}")
            logger.snipe(f"[{timestamp}] Message deleted in #{message.channel} ({message.guild}): {message.content}")

        # Send the deleted message content to audit logging channel
        with open("database.json", 'r', encoding="utf-8") as f: data = json.load(f)
        if data["audit_channel"][str(message.guild.id)] is not None:
            localembed = discord.Embed(title=f"Message deleted in #{message.channel.name} <t:{round(dts)}:R>", description=message.content, color=discord.Color.red())
            localembed.set_footer(icon_url=message.author.avatar, text=f"This message was sent by {author_name}")
            channel = client.get_channel(data["audit_channel"][str(message.guild.id)])
            await channel.send(embed=localembed)

@client.event
async def on_message_edit(message_before, message_after):
    if not message_after.author.bot:
        generate_data_entries(message_before.guild.id)

        dts = time.time()

        # Perform formatting for new Discord usernames.
        author_name: str = message_before.author.name
        author_name_split = author_name.split("#")
        if author_name_split[-1] == 0:
            author_name = author_name_split[0]

        # Save the edited message content to database
        editsnipe_data[str(message_before.guild.id)][str(message_before.channel.id)]["latest"] = {
            "original_content": message_before.content,
            "edited_content": message_after.content,
            "author_name": author_name,
            "time_stamp": str(round(dts))
        }
        editsnipe_data[str(message_before.guild.id)][str(message_before.channel.id)][str(message_before.author.id)] = {
            "original_content": message_before.content,
            "edited_content": message_after.content,
            "author_name": author_name,
            "time_stamp": str(round(dts))
        }

        # Log the edited message content to the client deleted message log.
        if bool(editsnipe_log):
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"[{timestamp}] Message edited in #{message_before.channel} ({message_before.guild}):\n   Old message: {message_before.content}\n   New message: {message_after.content}")
            logger.editsnipe(f"[{timestamp}] Message edited in #{message_before.channel} ({message_before.guild}):\n   Old message: {message_before.content}\n   New message: {message_after.content}")

        # Send the edited message content to audit logging channel
        with open("database.json", 'r', encoding="utf-8") as f: data = json.load(f)
        if data["audit_channel"][str(message_before.guild.id)] is not None:
            localembed = discord.Embed(title=f"Message edited in #{message_before.channel.name} <t:{round(dts)}:R>", description=f'**Message before**:```{message_before.content}```\n**Message after**:```{message_after.content}```', color=discord.Color.orange())
            localembed.set_footer(icon_url=message_before.author.avatar, text=f"This message was edited by {author_name}")
            channel = client.get_channel(data["audit_channel"][str(message_before.guild.id)])
            await channel.send(embed=localembed)

# Commands
@client.slash_command(
    name="help",
    description="Need some help?"
)
async def help(ctx: ApplicationContext):
    localembed = discord.Embed(title='Command Help', description=f'This bot uses Discord slash commands. (`/`)\n\n`/snipe`: See the most recently deleted message in this channel.\n`/editsnipe`: See the most recently edited message in this channel.\n`/set_audit_channel`: Set a channel to send all deleted and edited message audit logs to. (needs __Manage Channels__ permission)`', color=discord.Color.random())
    await ctx.send(embed=localembed)

@client.slash_command(
    name="snipe",
    description="Fetch the latest deleted message in this channel."
)
@option(name="user", description="Snipe message content in the channel from a specific user.", type=discord.User, default=None)
async def snipe(ctx: ApplicationContext, user: discord.User = None):
    """Fetch the latest deleted message in this channel."""
    if user is not None:
        try:
            data = snipe_data[str(ctx.guild.id)][str(ctx.channel.id)][str(user.id)]
            localembed = discord.Embed(title=f"Last deleted message from **{user.display_name}** in #{ctx.channel.name} <t:{data['time_stamp']}:R>", description=data["content"], color=discord.Color.random())
            localembed.set_footer(icon_url=ctx.author.avatar, text=f"This message was sent by {data['author_name']}")
            await ctx.respond(embed=localembed)
        except KeyError: await ctx.respond(f"There are no recently deleted messages in <#{ctx.channel.id}> from {user.display_name}")
    else:
        try:
            data = snipe_data[str(ctx.guild.id)][str(ctx.channel.id)]["latest"]
            localembed = discord.Embed(title=f"Last deleted message in #{ctx.channel.name} <t:{data['time_stamp']}:R>", description=data["content"], color=discord.Color.random())
            localembed.set_footer(icon_url=ctx.author.avatar, text=f"This message was sent by {data['author_name']}")
            await ctx.respond(embed=localembed)
        except KeyError: await ctx.respond(f"There are no recently deleted messages in <#{ctx.channel.id}>")

@client.slash_command(
    name="editsnipe",
    description="Fetch the latest edited message in this channel."
)
async def editsnipe(ctx: ApplicationContext):
    """Fetch the latest edited message in this channel."""
    try:
        data = editsnipe_data[str(ctx.guild.id)][str(ctx.channel.id)]["latest"]
        localembed = discord.Embed(title=f"Last edited message in #{ctx.channel.name} <t:{data['time_stamp']}:R>", description=f'**Message before**:```{data["original_content"]}```\n**Message after**:```{data["edited_content"]}```', color=discord.Color.random())
        localembed.set_footer(icon_url=ctx.author.avatar, text=f"This message was edited by {data['author_name']}")
        await ctx.respond(embed=localembed)
    except KeyError: await ctx.respond(f'There are no recently edited messages in <#{ctx.channel.id}>')

@client.slash_command(
    name="set_audit_channel",
    description="Set a channel to send all deleted and edited messages to."
)
@commands.has_permissions(manage_channels=True)
@option(name="channel", description="The channel that you want to set for audit logs. (leave blank to disable audit logging)", type=discord.TextChannel, default=None)
async def set_audit_channel(ctx: ApplicationContext, channel: discord.TextChannel = None):
    """Set a channel to send all deleted and edited messages to."""
    try:
        with open("database.json", 'r', encoding="utf-8") as f: data = json.load(f)  # Load bot database temporarily into a new variable
        if channel is not None: data["audit_channel"][str(ctx.guild_id)] = channel.id
        else: data["audit_channel"][str(ctx.guild_id)] = None
        with open("database.json", 'w+', encoding="utf-8") as f: json.dump(data, f, indent=4)  # Save modified datbaase to local machine
        if channel is not None:
            localembed = discord.Embed(description=f"**{ctx.guild.name}**'s audit log channel has been successfully set to {channel.mention}.", color=discord.Color.green())
            await ctx.respond(embed=localembed, ephemeral=True)
            channel_ctx = client.get_channel(channel.id)
            localembed1 = discord.Embed(title="Audit Channel Set", description="This channel has been set as this server's audit log channel.\nThis means that all deleted and edited message audit logs will appear here.\n\nIf you would like to turn these off, run `/set_audit_channel`.", color=discord.Color.random())
            localembed1.set_footer(icon_url=ctx.author.avatar, text=f"This action has been performed by {ctx.author.display_name}")
            await channel_ctx.send(embed=localembed1)
        else:
            localembed = discord.Embed(description=f"Deleted/Edited message audit logging for **{ctx.guild.name}** has been successfully disabled.", color=discord.Color.green())
            await ctx.respond(embed=localembed, ephemeral=True)
    except MissingPermissions: return await ctx.respond("You can't use this command!", ephemeral=True)

# Initialization
token = auth.get_token()
try: client.run(token)
except Exception as exc:
    print(f"[main/CLIENT] Error: Unable to start client: {type(exc).__name__}: {exc}")
    raise SystemExit
