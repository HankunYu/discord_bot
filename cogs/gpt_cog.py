import discord, sys, re
from discord import app_commands
from discord.ext import commands
sys.path.append("..") 
import gpt

class Cog(commands.Cog):
    on_conversion = False
    current_channel = None

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # listen to on_ready event and print bot info when bot is ready
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'bot login - {self.bot.user}')
        game = discord.Game("看电影中...")
        await self.bot.change_presence(status=discord.Status.idle, activity=game)
        slash = await self.bot.tree.sync()
        print(f"已载入 {len(slash)} 个指令")

    # listen to on_message event and reply to user message
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author == self.bot.user:
            return

        if self.bot.user.mentioned_in(message) or self.on_conversion:
            msg  = re.sub(r'<.*?>', '', message.content)
            self.on_conversion = True
            self.current_channel = message.channel
            reply = gpt.generate_reply(msg)
            if reply != None:
                await message.channel.send(reply)
            else:
                await message.channel.send("啊好像哪里出错了...这不应该，你再试试？不行就算了。")
            game = discord.Game("模仿GPT-3.5中...")
            await self.bot.change_presence(status=discord.Status.online, activity=game)

    # slash command
    @app_commands.command(description="停止GPT对话")
    async def stop(self, interaction: discord.Interaction):
        game = discord.Game("看电影中...")
        self.on_conversion = False
        await self.bot.change_presence(status=discord.Status.idle, activity=game)
        await interaction.response.send_message("^^")

async def setup(bot : commands.Bot):
    await bot.add_cog(Cog(bot))