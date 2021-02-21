
import logging
from utils.record import record_usage
from discord.ext import commands

from utils import embeds

log = logging.getLogger(__name__)


class GeneralCommandsCog(commands.Cog):
    """GeneralCommandsCog"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.before_invoke(record_usage)
    @commands.command(name="pfp", aliases=["avi", "pp", "avatar", "profilepic"])
    async def pfp(self, ctx, user=None):
        """ Returns the profile picture of the invoker or the mentioned user. """

        embed = embeds.make_embed(context=ctx)

        # Attempt to return the avatar of a mentioned user if the parameter was not none.
        if user is not None:
            user_strip = int(user.strip("<@!>"))
            member = ctx.message.guild.get_member(user_strip)
            if member:
                embed.set_image(url=member.avatar_url)
            else:
                raise commands.UserNotFound(user)
        # Otherwise, assume the invoker just wanted their only avatar and return that.
        else:
            embed.set_image(url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="userinfo", aliases=["info", "user"])
    async def info(self, ctx, user=None):
        """ Returns the user info of the invoker or the mentioned user. """

        member = None

        # Attempt to return the avatar of a mentioned user if the parameter was not none.
        if user is not None:
            user_strip = int(user.strip("<@!>"))
            member = ctx.message.guild.get_member(user_strip)
        # Otherwise, assume the invoker just wanted their only avatar and return that.
        else:
            member = ctx.author
        
        if member:
            embed = embeds.make_embed(context=ctx).set_thumbnail(url=member.avatar_url)
            embed.add_field(name="User ID", value=member.id, inline=True)
            embed.add_field(name="Username", value=f"{member.name}#{member.discriminator}", inline=True)
            embed.add_field(name="Nickname", value=member.nick, inline=True)
            embed.add_field(name="Joined Guild at", value=member.joined_at, inline=True)
            embed.add_field(name="Joined Discord at", value=member.created_at, inline=True)
            embed.add_field(name="Is Bot?", value={True:"Yes", False:"No"}.get(member.bot), inline=True)
            
            role_list = member.roles[1:]
            role_mentions_str = ""
            for x in role_list:
                role_mentions_str+=x.mention+" "
            
            embed.add_field(name="Roles", value=role_mentions_str, inline=False)
                
        else:
            raise commands.UserNotFound(member)
        
        await ctx.send(embed=embed)
        

def setup(bot) -> None:
    """ Load the GeneralCog cog. """
    bot.add_cog(GeneralCommandsCog(bot))
    log.info("Loaded General Commands cog.")