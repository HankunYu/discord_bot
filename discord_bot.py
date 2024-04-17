import discord, discord.webhook, asyncio, os
from discord.ext import commands
from shared_variables import current_channel, discord_token
from threading import Thread

"""
bot
"""

on_conversion = False
current_channel = None
intents = discord.Intents.all()
client = commands.Bot(command_prefix='$', intents=intents)


# Load cogs
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

async def unload_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.unload_extension(f"cogs.{filename[:-3]}")
            
async def send_message(reply, embed=None, view=None):
    await current_channel.send(reply, embed=embed, view=view)

async def main():
    async with client:
        await load_extensions()
        await client.start(discord_token)
        
async def stop():
    # await client.close()
    await unload_extensions()
    
def start_bot():
    asyncio.run(main())
    
async def start():
    async with client:
        await load_extensions()
        await client.start(discord_token)
        
def run_it_forever(loop):
    loop.run_forever()
    
if __name__ == '__main__':
    start_bot()
