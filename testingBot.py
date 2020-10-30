from typing import List
import discord
import random
from discord import embeds
import requests
import time
import asyncio
from waifuUtils import *
from anilistTest import *

client = discord.Client()
botPrefix = '*'


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))




@client.event
async def on_message(message):
    if message.content.startswith(botPrefix+"help"):
        embedVar = discord.Embed(title="Requested by "+message.author.display_name,
                                 description="Displays help.", color=0x5678fc)
        embedVar.add_field(
            name=botPrefix+"neko", value="Sends an image of a nekomimi. Nyaa ~", inline=False)
        embedVar.add_field(name=botPrefix+"waifu",
                           value="Sends an image of a waifu.", inline=False)
        embedVar.add_field(name=botPrefix+"random N",
                           value="Generates a random number between 0 to N.", inline=False)
        embedVar.add_field(name=botPrefix+"find CHARACTER_NAME",
                           value="Searches info about character on AniList and shows it in a slideshow.(WIP)", inline=False)
        embedVar.add_field(name=botPrefix+"images",
                           value="Generates waifu images.")
        # embedVar.add_field(
        #   name=botPrefix+"roulette [BET VALUE] or [BET COLOR]", value="WIP.", inline=False)

    if message.content.startswith(botPrefix+"random "):
        embedVar = discord.Embed(title="Requested by "+message.author.display_name,
                                 description="Random number generating!", color=0x00ff00)
        try:
            n = float(message.content.split(' ')[1])
            embedVar.add_field(name="Random Number",
                               value=random.randrange(round(abs(n), 0)), inline=False)
        except:
            embedVar.add_field(
                name="ERROR.", value="Please enter a valid, non-zero number for range.", inline=False)

    if message.content.startswith(botPrefix+"neko"):
        URL = "https://nekos.life/api/neko"
        r = requests.get(url=URL)
        neko = (r.json()['neko'])
        print(neko)
        embedVar = discord.Embed(
            title="Nekos!", description="Nyaa ~", color=0xccff00).set_image(url=neko)

    if message.content.startswith(botPrefix+"waifu"):
        embedVar = discord.Embed(
            title="Waifu!", color=0x00ffcc).set_image(url=get_waifu())

    if message.content.startswith(botPrefix+"images"):
        #Thank you Stalker and Subby senpai ~!
        waifus = get_waifus()["files"]
        waifuList = []
        n=1
        page_no = 1
        embedVar = discord.Embed(
            title="Waifus!", description="Requested by: "+message.author.display_name, color=0xfac105)
        msgId = await message.channel.send(embed=embedVar)
        await msgId.add_reaction('⏮')
        await msgId.add_reaction('🟥')
        await msgId.add_reaction('⏭')
        for x in waifus:
            waifuList.append(x)
            n+=1
        
        def check(reaction, user):
            return user == message.author and str(reaction.emoji) in ['⏮', '⏭','🟥']
        while True:
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await msgId.delete()
                break
            else:
                if (reaction.emoji == '⏭' and page_no <= n):
                    page_no+=1
                    embedVar.set_image(url=waifuList[page_no])
                    await msgId.edit(embed=embedVar)
                elif(reaction.emoji == '⏮' and page_no >= 1):
                    page_no-=1
                    embedVar.set_image(url=waifuList[page_no])
                    await msgId.edit(embed=embedVar)
                elif(reaction.emoji == '🟥'):
                    await msgId.delete()
                    break
                await reaction.remove(message.author)
                print(page_no)
        

    if message.content.startswith(botPrefix+"roulette "):
        embedVar = discord.Embed(
            title="Roulette.", description="Requested by:"+message.author.display_name, color=0xab3dff)
        bet = message.content.split(' ')[1]
        if (bet.isnumeric()):
            if (int(bet) <= 37):
                return
            else:
                embedVar.add_field(
                    name="Roulette bet values range from 1 to 37.", value="Please try again.", inline=False)

        elif (bet == "BLACK" or bet == "RED"):
            return

        else:
            embedVar.add_field(name="You can't bet on that.",
                               value="Try again.", inline=False)

    if message.content.startswith(botPrefix+"search "):
        message_content = message.content.split(' ')
        waifu_name = ""
        embedVar = discord.Embed(
            title="Requested by:"+message.author.display_name, description="Waifu search!", color=0xff6ec7)
        for temp in message_content:
            if (temp != botPrefix+"search"):
                waifu_name = waifu_name+temp+" "
        print(waifu_name)
        waifu_info = searchWaifu(waifu_name)
        embedVar.set_thumbnail(url=waifu_info["image"]["large"])
        try:
        	embedVar.add_field(
            	name="Name:", value=waifu_info["name"]["full"]+"("+waifu_info["name"]["native"]+")", inline=False)
        except:
        	embedVar.add_field(name="Name:", value= waifu_info["name"]["full"], inline=False)
        embedVar.add_field(name="Anilist URL:",
                           value=waifu_info["siteUrl"], inline=False)

    if message.content.startswith(botPrefix+"find "):
        message_content = message.content.split(' ')
        waifu_name = ""
        embedVar = discord.Embed(
            title="Requested by:"+message.author.display_name, description="Waifu search!", color=0xff6ec7)
        for temp in message_content:
            if (temp != botPrefix+"find"):
                waifu_name = waifu_name+temp+" "
        print(waifu_name)
        waifu_info = searchWaifus(waifu_name)
        delay = 4
        embedVar = discord.Embed(
            title="Waifu search!", description="Results", color=0xff69b4).set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
        msgId = await message.channel.send(embed=embedVar)
        for waifu in waifu_info:
            embedVar = discord.Embed(
                title="Search Results.", description="Slideshow time: 4 seconds.", color=0xff69b4).set_thumbnail(url=waifu["image"]["large"]).set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
            embedVar.add_field(
                name="Name:", value=waifu["name"]["full"], inline=False)
            embedVar.add_field(name="Anilist URL:",
                               value=waifu["siteUrl"], inline=False)
            await msgId.edit(embed=embedVar)
            time.sleep(5)
        await msgId.delete()

    try:
        await message.channel.send(embed=embedVar)
    except:
        return
 
client.run('BOT_API_KEY_HERE')

