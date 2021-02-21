"""
This File is for demonstrating and used as a template for future cogs.
"""

import logging

from discord.ext import commands
from utils import embeds
from utils.record import record_usage


# Enabling logs
log = logging.getLogger(__name__)


class WaifuRoulette(commands.Cog):
    """Waifu Roulette Cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.before_invoke(record_usage)
    @commands.group(aliases=['w', 'wr', 'r', 'rl', 'wrl'])
    async def roulette(self, ctx):
        if ctx.invoked_subcommand is None:
            # Send the help command for this group
            await ctx.send_help(ctx.command)

    
    @roulette.commands(name="help")
    async def rl_help(self, ctx):
        """ Sends the commands list for the waifu roulette """
        await ctx.send_help(ctx.command)

    

# The setup function below is necessary. Remember we give bot.add_cog() the name of the class in this case SimpleCog.
# When we load the cog, we use the name of the file.
def setup(bot) -> None:
    """Load the WaifuRoulette cog."""
    bot.add_cog(WaifuRoulette(bot))
    log.info("Loaded Waifu Roulette cog.")
