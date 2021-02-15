import discord
from discord.ext import commands
import constants
import glob

bot = commands.Bot(
    command_prefix=constants.Bot.prefix,
    intents=discord.Intents(messages=True, guilds=True, members=True, bans=True, reactions=True),
    case_insensitive=True)

@bot.event
async def on_ready():
    """Called when the client is done preparing the data received from Discord.
    For more information:
    https://discordpy.readthedocs.io/en/stable/api.html#discord.on_ready
    """
    print(f"Logged in as: {bot.user.name}#{bot.user.discriminator}")
    print(f"discord.py version: {discord.__version__}\n")

    # Adding in a activity message when the bot begins.
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name=f"with [REDACTED]."
        )
    )


if __name__ == '__main__':
    # Recursively loads in all the cogs in the folder named cogs.
    # Skips over any cogs that start with '__' or do not end with .py.
    for cog in glob.iglob("cogs/**/[!^_]*.py", recursive=True):
        try:
            if "\\" in cog:  # Fix pathing on Windows.
                bot.load_extension(cog.replace("\\", ".")[:-3])
            else:  # Fix pathing on Linux.
                bot.load_extension(cog.replace("/", ".")[:-3])
        except:
            continue

    # Finally, run the bot.
    bot.run(constants.Bot.token)

