import discord
import random
import requests
import json

client = discord.Client()
botPrefix = '*'


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(botPrefix+"help"):
        embedVar = discord.Embed(title="Requested by "+message.author.display_name,
                                 description="Displays help.", color=0x5678fc)
        embedVar.add_field(
            name=botPrefix+"neko", value="Sends an image of a nekomimi. Nyaa ~", inline=False)
        embedVar.add_field(name=botPrefix+"waifu",
                           value="Sends an image of a waifu.", inline=False)
        embedVar.add_field(name=botPrefix+"random N",
                           value="Generates a random number between 0 to N.", inline=False)
        # embedVar.add_field(
        #   name=botPrefix+"roulette [BET VALUE] or [BET COLOR]", value="WIP.", inline=False)

    if message.content.startswith(botPrefix+"random "):
        embedVar = discord.Embed(title="Requested by "+message.author.display_name,
                                 description="Random number generating!", color=0x00ff00)
        try:
            n = int(message.content.split(' ')[1])
            embedVar.add_field(name="Random Number",
                               value=random.randrange(n), inline=False)
        except:
            embedVar.add_field(
                name="ERROR.", value="Please enter a number for range.", inline=False)

    if message.content.startswith(botPrefix+"neko"):
        URL = "https://nekos.life/api/neko"
        r = requests.get(url=URL)
        neko = (r.json()['neko'])
        embedVar = discord.Embed(
            title="Nekos!", description="Nyaa ~", color=0xccff00).set_image(url=neko)

    if message.content.startswith(botPrefix+"waifu"):
        URL = "https://waifu.pics/api/sfw/waifu"
        r = requests.get(url=URL)
        waifu = r.json()['url']
        embedVar = discord.Embed(
            title="Waifu!", color=0x00ffcc).set_image(url=waifu)

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
    else:
        return

    try:
        await message.channel.send(embed=embedVar)
    except:
        return

client.run('NzY1MTA1ODE1NTAxMDEyOTky.X4P-UQ.ePdeBOVLY-7NkCppGTw6qAwMN-Q')
