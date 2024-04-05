# Imports
import os
import time
import os.path
import discord
import json
import framework.auth
import framework.logger
from datetime import datetime
from discord import ApplicationContext
from discord.ext import commands
from discord.ext.commands import *

# Variables
auth = framework.auth.Auth()
botVer = 'v1.2.1'
if os.name == 'nt': os.system('cls')
else: os.system('clear')
intents = discord.Intents.default()
intents.message_content = (True)
client = discord.Bot(intents=intents)  # READ COMMENT AT LINE 13 FOR MORE INFO
global startTime
startTime = time.time()
config = auth.get_raw()

# Initialize dicts for snipe and editsnipe data
snipe_data = {}
editsnipe_data = {}

# Pre-Initialization Commands
auth.initial_setup()  # Check if bot token and owner username are missing and ask user if they want to add it

owner = auth.get_owner_name()

snipe_log:bool = config[str("config")][str("logs")]["snipe"]
editsnipe_log:bool = config[str("config")][str("logs")]["editsnipe"]

if not os.path.isdir("logs"):  # Create logs dir and all log files if they are missing from current working directory
    os.mkdir("logs")
    open("logs/snipe.log", 'x', encoding="utf-8")
    open("logs/editsnipe.log", 'x', encoding="utf-8")
    open("logs/errors.log", 'x', encoding="utf-8")

logger = framework.logger.Logger()

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
async def on_message_delete(message):
    if not message.author.bot:
        dts = time.time()
        snipe_data[str(message.channel.id)] = {
            "author": message.author,
            "content": message.content,
            "author_name": message.author,
            "time_stamp": str(dts)
        }
        if bool(snipe_log):
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"[{timestamp}] Message deleted in #{message.channel} ({message.guild}):\n   Message content: {message.content}")
            logger.snipe(f"[{timestamp}] Message deleted in #{message.channel} ({message.guild}): {message.content}")
        else: pass

@client.event
async def on_message_edit(message_before, message_after):
    if not message_after.author.bot:
        dts = time.time()
        editsnipe_data[str(message_before.channel.id)] = {
            "message_author": message_before.author,
            "original_content": message_before.content,
            "edited_content": message_after.content,
            "author_name": message_before.author,
            "time_stamp": str(dts)
        }
        if bool(editsnipe_log):
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"[{timestamp}] Message edited in #{message_before.channel} ({message_before.guild}):\n   Old message: {message_before.content}\n   New message: {message_after.content}")
            logger.editsnipe(f"[{timestamp}] Message edited in #{message_before.channel} ({message_before.guild}):\n   Old message: {message_before.content}\n   New message: {message_after.content}")
        else: pass

# Commands
@client.slash_command(
    name="help",
    description="Need some help?"
)
async def help(ctx: ApplicationContext):
    localembed = discord.Embed(title='Command Help', description=f'This bot uses Discord slash commands. (`/`)\n\n`/snipe`: See the most recently deleted message in this channel.\n`/editsnipe`: See the most recently edited message in this channel.', color=discord.Color.random())
    await ctx.send(embed=localembed)

@client.slash_command(
    name="snipe",
    description="Fetch the latest deleted message in this channel."
)
async def snipe(ctx: ApplicationContext):
    try:
        data = snipe_data[str(ctx.channel.id)]
        localembed = discord.Embed(title=f"Last deleted message in #{ctx.channel.name}", description=data["content"], color=discord.Color.random())
        localembed.set_footer(text=f"This message was sent by {data['author_name']}  <t:{data['time_stamp']}:R>")
        await ctx.respond(embed=localembed)
    except KeyError: await ctx.respond(f"There are no recently deleted messages in <#{ctx.channel.id}>")

@client.slash_command(
    name="editsnipe",
    description="Fetch the latest edited message in this channel."
)
async def editsnipe(ctx: ApplicationContext):
    try:
        data = editsnipe_data[str(ctx.channel.id)]
        localembed = discord.Embed(title=f"Last edited message in #{ctx.channel.name}", description=f'**Message before**:```{data["original_content"]}```\n**Message after**:```{data["edited_content"]}```', color=discord.Color.random())
        localembed.set_footer(text=f"This message was edited by {data['author_name']} <t:{data['time_stamp']}:R>")
        await ctx.respond(embed=localembed)
    except KeyError: await ctx.respond(f'There are no recently edited messages in <#{ctx.channel.id}>')

# Initialization
token = auth.get_token()
try: client.run(token)
except Exception as exc:
    print(f"[main/CLIENT] Error: Unable to start client: {type(exc).__name__}: {exc}")
    raise SystemExit
