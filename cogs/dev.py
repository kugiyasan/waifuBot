import discord
from discord.ext import commands

class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        pass
        # print(discord.Permissions.send_messages)

def setup(bot):
    bot.add_cog(Dev(bot))

