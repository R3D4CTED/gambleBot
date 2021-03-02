import asyncio
import subprocess
from utils.record import record_usage
import discord
from discord.ext import commands
from os import path

from utils import embeds
from utils import gc_utils

import logging

log = logging.getLogger(__name__)

class GcloneCommandsCog(commands.Cog):
    """GcloneCommandsCog"""
    
    @commands.before_invoke(record_usage)
    @commands.is_owner()
    @commands.group(name="gclone", aliases=["g", "gc"])
    async def gclone(self, ctx):
        if ctx.invoked_subcommand is None:
            # Send the help command for this group
            await ctx.send_help(ctx.command)
        
    @gclone.command(name="copy", aliases=['c', 'cp'])
    async def gc_copy(self, ctx, src_id: str, dest_id: str):
        """Copies from specified source folder to destination folder."""
        
        embed = embeds.make_embed(title="Copy", color='green', context=ctx)
        embed.add_field(name="Source Folder ID:", value=src_id, inline=True)
        embed.add_field(name="Destination Folder ID:", value=dest_id, inline=True)
        msg = await ctx.send(embed=embed)
        
        cmd = (f'gclone --config=rc.conf copy GC:{{{src_id}}} GC:{{{dest_id}}} {gc_utils.SRflag}')
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            encoding='utf-8',
            errors='replace'
        )
        embed.add_field(name="Output", value=None, inline=True)
        while True:
            realtime_output = process.stdout.readline()
            if realtime_output == '' and process.poll() is not None:
                break
            if realtime_output:
                try:
                    realtime_output = realtime_output.strip()
                    print(realtime_output, flush=True)
                    embed.set_field_at(index=2, name="Output", value=f"```\n{realtime_output}\n```", inline=False)
                except:
                    continue
            
            await msg.edit(embed=embed)

    
def setup(bot) -> None:
    """ Load the GcloneCommandsCog cog. """
    if (path.exists("accounts") and path.exists("gclone.exe")):
        bot.add_cog(GcloneCommandsCog(bot))
        log.info("Loaded Gclone commands")
    else:
        log.error("Gclone executable and/or service accounts not found.")
