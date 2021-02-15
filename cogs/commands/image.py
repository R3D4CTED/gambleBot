import discord
from discord import Color
from discord.ext import commands

from utils import embeds
from utils import imageFetchUtils
from utils import checks

class ImageCommandsCog(commands.Cog):
    """SimpleCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="neko", aliases=['nyan', 'nyaa', 'nya'])
    async def neko(self, ctx):
        """ Displays cute Nekomimis! """
        embed = embeds.make_embed(title="Nyaa ~", description="Nekomimis!", context=ctx).set_image(url=imageFetchUtils.get_neko())
        embed.color = discord.Color(0xccff00)
        await ctx.send(embed=embed)

    @commands.command(name="waifu")
    async def waifu(self, ctx):
        """ Displays waifu pics! """
        embed = embeds.make_embed(title="Waifu!", context=ctx).set_image(url=imageFetchUtils.get_waifu())
        embed.color = discord.Color(0x00ffcc)
        await ctx.send(embed=embed)
    
    @commands.check(checks.is_nsfw)
    @commands.command(name="xneko", aliases=['xnyan', 'xnyaa', 'xnya', 'nyanx', 'nyaax', 'nyax', 'nekox'])
    async def xneko(self, ctx):
        
        """ Displays lewd Nekomimis! """
        embed = embeds.make_embed(title="Nyaa ~", description="Lewd!", context=ctx).set_image(url=imageFetchUtils.get_xneko())
        embed.color = discord.Color(0xccff00)
        await ctx.send(embed=embed)

    @commands.check(checks.is_nsfw)
    @commands.command(name="xwaifu", aliases=['waifux'])
    async def xwaifu(self, ctx):
        """ Displays lewd waifu pics! """
        embed = embeds.make_embed(title="Waifu!", context=ctx).set_image(url=imageFetchUtils.get_waifu(lewd="nsfw"))
        embed.color = discord.Color(0x00ffcc)
        await ctx.send(embed=embed)
    


# The setup function below is necessary. Remember we give bot.add_cog() the name of the class in this case SimpleCog.
# When we load the cog, we use the name of the file.
def setup(bot) -> None:
    """Load the SimpleCog cog."""
    bot.add_cog(ImageCommandsCog(bot))
    print("Loaded Image Commands Cog.")