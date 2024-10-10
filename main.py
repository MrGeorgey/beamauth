import discord
import os
import asyncio

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

client = commands.Bot(command_prefix="$", intents=discord.Intents.all())

TOKEN = os.getenv('TOKEN')
OWNERID = os.getenv('OWNER')

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await client.tree.sync()

async def load():
    await client.load_extension("verify")
async def main():
    async with client:
        await load()
        await client.start(TOKEN)

asyncio.run(main())