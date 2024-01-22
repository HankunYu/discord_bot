import discord, gpt, re, discord.webhook, asyncio, cogs.moviepilot_cog as moviepilot_cog, os
from discord import app_commands
from discord.ui import Button, View
from discord.ext import commands
from shared_variables import current_channel, discord_token

"""
bot 本体.
"""

on_conversion = False
current_channel = None
intents = discord.Intents.all()
client = commands.Bot(command_prefix='$', intents=intents)
    
@client.command(name="sync")
async def sync(ctx):
    slash = await client.tree.sync()
    await ctx.send(f"載入 {len(slash)} 個斜線指令")

   

# Load cogs
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

async def send_message(reply, embed=None, view=None):
    await current_channel.send(reply, embed=embed, view=view)

async def main():
    async with client:
        await load_extensions()
        await client.start(discord_token)

if __name__ == '__main__':
    asyncio.run(main())