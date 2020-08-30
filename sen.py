# https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html
# https://github.com/runarsf/rufus

import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

from cogs.utils.deleteMessage import deleteMessage
from cogs.utils.dbms import conn, cursor

load_dotenv()


async def prefixes(bot: commands.Bot, message: discord.Message):
    prefix = "xd"
    if message.guild != None:
        with conn:
            cursor.execute(
                "SELECT command_prefix FROM guilds WHERE id = %s", (message.guild.id,))
            temp = cursor.fetchone()
            if temp and temp[0]:
                prefix = temp[0]

    return commands.when_mentioned_or(prefix + " ", prefix)(bot, message)

description = """Senko-san wants to pamper you"""

bot = commands.Bot(command_prefix=prefixes,
                   description=description,
                   activity=discord.Game(name="xd help | xd about"))


def getExtensions():
    for path in ("cogs", "cogs/Games"):
        for f in os.listdir(path):
            pathname = os.path.join(path, f)
            if os.path.isfile(pathname):
                yield pathname[:-3].replace("/", ".").replace("\\", ".")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


@bot.command(hidden=True, aliases=["rl"])
@commands.is_owner()
async def reload(ctx: commands.Context):
    """Reloads the bot extensions without rebooting the entire program"""
    await deleteMessage(ctx)

    try:
        for ext in getExtensions():
            try:
                bot.reload_extension(ext)
            except commands.errors.ExtensionNotLoaded:
                bot.load_extension(ext)
    except:
        await ctx.send("Reloading failed")
        raise

    print("\033[94mReloading successfully finished!\033[0m\n")


@bot.command(hidden=True)
@commands.is_owner()
async def logout(ctx: commands.Context):
    await deleteMessage(ctx)
    await bot.logout()


if __name__ == "__main__":
    for ext in getExtensions():
        bot.load_extension(ext)

    bot.run(os.environ["DISCORD_TOKEN"])
