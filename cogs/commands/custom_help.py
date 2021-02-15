
from discord.ext import commands

from utils import embeds




class GcloneCommandsCog(commands.Cog):
    """GcloneCommandsCog"""
    def __init__(self, bot):
        self.bot = bot

    
        

def setup(bot) -> None:
    """ Load the GeneralCog cog. """
    bot.add_cog(GcloneCommandsCog(bot))