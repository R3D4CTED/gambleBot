import discord
import random
import requests
import json
import time
from waifuUtils import *
from anilistTest import searchWaifu

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
        embedVar.add_field(name=botPrefix+"search CHARACTER_NAME",
                           value="Searches info about character on anilist.(WIP)", inline=False)
        embedVar.add_field(name=botPrefix+"waifus x", value="Generates waifu images with x seconds of delay between each.(WIP)")
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

    if message.content.startswith(botPrefix+"waifus "):
        waifus=get_waifus()["files"]
        delay = int(message.content.split(' ')[1])
        page_no=1
        embedVar = discord.Embed(title="Waifus!", description="Requested by: "+message.author.display_name, color=0xfac105)
        msgId = await message.channel.send(embed=embedVar)
        for x in waifus:
        	print(str(page_no)+" : "+x)
        	embedVar.set_image(url=x)
        	time.sleep(delay)
        	await msgId.edit(embed=embedVar)
        	page_no+=1



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
        embedVar.add_field(
            name="Name:", value=waifu_info["name"]["full"]+"("+waifu_info["name"]["native"]+")", inline=False)
        embedVar.add_field(name="Description:", value="||" +
                           waifu_info["description"]+"||", inline=False)
        embedVar.add_field(name="Anilist URL:",
                           value=waifu_info["siteUrl"], inline=False)

    try:
        await message.channel.send(embed=embedVar)
    except:
        return

client.run('BOT_API_HERE')
