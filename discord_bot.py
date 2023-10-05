import discord
import gpt
import asyncio
import re
import discord.webhook
from discord.ui import Button, View
from shared_variables import current_channel, discord_token, converstation_timer

intents = discord.Intents.default()
intents.message_content = True

on_conversion = False
timer = converstation_timer
current_channel = None
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    asyncio.create_task(countdown())

@client.event
async def on_message(message):
    
    global on_conversion
    global timer
    global current_channel

    if message.author == client.user:
        return

    if client.user.mentioned_in(message) or on_conversion:
        print('get mentioned ', timer)
        msg  = re.sub(r'<.*?>', '', message.content)
        timer = converstation_timer  # 设置5分钟的倒计时
        on_conversion = True
        current_channel = message.channel
        reply = gpt.define_command(msg)
        print('reply: ', reply)
        if reply != None:
            await message.channel.send(reply)

async def countdown():
    global on_conversion
    global timer

    while True:
        if on_conversion:
            if timer > 0:
                timer -= 1
            else:
                on_conversion = False
                gpt.clear_chat_history()
                await send_message('我洗澡去了,有事请@我')
        await asyncio.sleep(1)

async def send_message(reply, embed=None, view=None):
    await current_channel.send(reply, embed=embed, view=view)

def run_bot():
    client.run(discord_token)