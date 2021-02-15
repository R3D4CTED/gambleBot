import discord.ext.commands
import discord

def is_nsfw(ctx) -> bool:
    return ctx.channel.is_nsfw()