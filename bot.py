import discord
import gpt
import asyncio
import re
import discord.webhook
from discord.ui import Button, View
from discord.ext import commands
from shared_variables import current_channel, discord_token, converstation_timer

"""
bot 本体.
只回应被@的消息,或者在对话中.
当对话超过5分钟没有回应,则bot会自动结束对话.
"""

intents = discord.Intents.default()
intents.message_content = True
on_conversion = False
timer = converstation_timer
current_channel = None
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

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

@client.command()
async def button_example(ctx):
    # 创建按钮
    button = Button(label="点击我", style=discord.ButtonStyle.primary, custom_id="my_button")

    # 创建视图
    view = View()
    view.add_item(button)

    # 发送消息并附上视图
    await ctx.send("这是一个按钮示例", view=view)

@client.event
async def on_button_click(interaction: discord.Interaction):
    if interaction.component.custom_id == "my_button":
        print("按钮被点击111！")
        await my_button_callback(interaction)

async def my_button_callback(interaction: discord.Interaction):
    await interaction.response.send_message("按钮被点击！")


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