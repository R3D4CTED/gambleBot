from typing import List
import discord
import random
import requests
import time
import asyncio
from waifuUtils import *
from anilistTest import *
from nhscript import *

client = discord.Client()
botPrefix = '*'
botPrefixW = ')'


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    status = 'with [REDACTED]. *Nyaa ~*'
    # set your custom status here. Displays as playing "status"
    await client.change_presence(activity=discord.Game(name=status))
    print(client.latency)


@client.event
async def on_message(message):
    if message.content.startswith(botPrefix+"help"):
        embedVar = discord.Embed(title="Requested by "+message.author.display_name,
                                 description="Displays help.", color=0x5678fc)
        embedVar.add_field(
            name=botPrefix+"neko", value="Sends an image of a nekomimi. Nyaa ~", inline=False)
        embedVar.add_field(name=botPrefix+"waifu",
                           value="Sends an image of a random waifu.", inline=False)
        embedVar.add_field(name=botPrefix+"images",
                           value="Generates random waifu images.")
        embedVar.add_field(name=botPrefix+"random N",
                           value="Generates a random number between 0 to N.", inline=False)
        embedVar.add_field(name=botPrefix+"find CHARACTER_NAME",
                           value="Searches info about character on AniList.", inline=False)
        # NSFW commands listing.
        if message.channel.is_nsfw():
            embedVar.add_field(name="NSFW",
                               value="These commands will work only in nsfw channels.", inline=False)
            embedVar.add_field(name=botPrefix+"get CHARACTER_NAME",
                               value="Searches info about character on AniList, with a fanart image from Danbooru(WIP)", inline=False)
            embedVar.add_field(name=botPrefix+"xwaifu",
                               value="Fetches one random NSFW waifu image.", inline=False)
            embedVar.add_field(name=botPrefix+"ximages",
                               value="Generates random NSFW waifus", inline=False)
            embedVar.add_field(name=botPrefix+"danbooru TAG",
                               value="Gets an image from Danbooru for the specified tag.", inline=False)
            embedVar.add_field(name=botPrefix+"digit 6_DIGITS",
                               value="Gets tags and information for the 6 digits provided.", inline=False)

        # deprecated commands
        # embedVar.add_field(
        #   name=botPrefix+"roulette [BET VALUE] or [BET COLOR]", value="WIP.", inline=False)

    if message.content.startswith(botPrefix+"ping"):
        await message.channel.send("Pong ~ 🏓. Latency is:"+str(round(client.latency*1000))+"ms")

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
        neko = get_neko()
        print(neko)
        embedVar = discord.Embed(
            title="Nekos!", description="Nyaa ~", color=0xccff00).set_image(url=neko)

    if message.content.startswith(botPrefix+"waifu"):
        waifu = get_waifu()
        print(waifu)
        embedVar = discord.Embed(
            title="Waifu!", color=0x00ffcc).set_image(url=waifu)

    if message.content.startswith(botPrefix+"xwaifu"):
        if not message.channel.is_nsfw():
            return

        xwaifu = get_xwaifu()
        print(xwaifu)
        embedVar = discord.Embed(
            title="Waifu!", color=0x00aacc).set_image(url=xwaifu)

    if message.content.startswith(botPrefix+"images"):
        waifus = get_waifus()["files"]
        waifuList = []
        n = 1
        page_no = 1
        embedVar = discord.Embed(
            title="Waifus!", description="Page number"+str(page_no)+" of "+str(n), color=0xfac105)
        msgId = await message.channel.send(embed=embedVar)
        await msgId.add_reaction('⏮')
        await msgId.add_reaction('🟥')
        await msgId.add_reaction('⏭')
        await msgId.add_reaction('💾')
        for x in waifus:
            print(x)
            waifuList.append(x)
            n += 1

        def check(reaction, user):
            return user == message.author and str(reaction.emoji) in ['⏮', '⏭', '🟥', '💾']
        while True:
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await msgId.delete()
                break
            else:
                if (reaction.emoji == '⏭' and page_no <= n):
                    page_no += 1
                    embedVar.set_image(url=waifuList[page_no])
                    await msgId.edit(embed=embedVar)
                elif(reaction.emoji == '⏮' and page_no >= 1):
                    page_no -= 1
                    embedVar.set_image(url=waifuList[page_no])
                    await msgId.edit(embed=embedVar)
                elif(reaction.emoji == '💾'):
                    await message.channel.send(embed=embedVar)
                elif(reaction.emoji == '🟥'):
                    await msgId.delete()
                    return
                await reaction.remove(message.author)
                print(page_no)

    if message.content.startswith(botPrefix+"ximages"):
        if not message.channel.is_nsfw():
            return

        waifus = get_xwaifus()["files"]
        waifuList = []
        n = 1
        page_no = 1
        embedVar = discord.Embed(
            title="Waifus!", description="Page number"+str(page_no)+" of "+str(n), color=0xfac105)
        msgId = await message.channel.send(embed=embedVar)
        await msgId.add_reaction('⏮')
        await msgId.add_reaction('🟥')
        await msgId.add_reaction('⏭')
        await msgId.add_reaction('💾')
        for x in waifus:
            waifuList.append(x)
            print(x)
            n += 1

        def check(reaction, user):
            return user == message.author and str(reaction.emoji) in ['⏮', '⏭', '🟥', '💾']
        while True:
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await msgId.delete()
                break
            else:
                if (reaction.emoji == '⏭' and page_no <= n):
                    page_no += 1
                    embedVar.set_image(url=waifuList[page_no])
                    await msgId.edit(embed=embedVar)
                elif(reaction.emoji == '⏮' and page_no >= 1):
                    page_no -= 1
                    embedVar.set_image(url=waifuList[page_no])
                    await msgId.edit(embed=embedVar)
                elif(reaction.emoji == '💾'):
                    await message.channel.send(embed=embedVar)
                elif(reaction.emoji == '🟥'):
                    await msgId.delete()
                    return
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

    if message.content.startswith(botPrefix+"find "):
        message_content = message.content.split(' ')
        waifu_name = ""
        embedVar = discord.Embed(
            title="Requested by:"+message.author.display_name, description="Waifu search!", color=0xff6ec7)

        for temp in message_content:

            if (temp != botPrefix+"find"):
                waifu_name = waifu_name+temp+" "

        print(waifu_name)
        channel = message.channel
        waifu_info = searchWaifus(waifu_name)
        waifu_names = []
        waifu_image = []
        waifu_url = []
        waifu_anime = []
        for waifu in waifu_info:
            waifu_names.append(waifu["name"]["full"])
            waifu_image.append(waifu["image"]["large"])
            waifu_url.append(waifu["siteUrl"])
            waifu_ani = waifu["media"]["nodes"]
            for anime in waifu_ani:
                waifu_anime.append(anime["title"]["userPreferred"])
                break

        page_no = 0
        embedVar = discord.Embed(title="Waifu search!", description="Generating results...",
                                 color=0xffabc7).set_thumbnail(url=waifu_image[page_no])
        embedVar.add_field(
            name="Name: ", value=waifu_names[page_no], inline=False)
        embedVar.add_field(name="Anime name:", value=waifu_anime[page_no])
        embedVar.add_field(name="AniList URL:",
                           value=waifu_url[page_no], inline=False)
        msgId = await channel.send(embed=embedVar)

        await msgId.add_reaction('⏮')
        await msgId.add_reaction('🟥')
        await msgId.add_reaction('⏭')
        await msgId.add_reaction('💾')

        def check(reaction, user):
            return user == message.author and str(reaction.emoji) in ['⏮', '⏭', '🟥', '💾']
        while True:
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await msgId.delete()
                break
            else:
                if (reaction.emoji == '⏭' and page_no <= len(waifu_name)-1):
                    page_no += 1

                elif(reaction.emoji == '⏮' and page_no >= 0):
                    page_no -= 1

                elif(reaction.emoji == '💾'):
                    await message.channel.send(embed=embedVar)

                elif(reaction.emoji == '🟥'):
                    await msgId.delete()
                    return

                try:
                    embedVar = discord.Embed(title="Waifu search!", description="Generating results...",
                                             color=0xffabc7).set_thumbnail(url=waifu_image[page_no])
                    embedVar.add_field(
                        name="Name: ", value=waifu_names[page_no], inline=False)
                    embedVar.add_field(name="Anime name:",
                                       value=waifu_anime[page_no])
                    embedVar.add_field(name="AniList URL:",
                                       value=waifu_url[page_no], inline=False)
                except:
                    await reaction.remove(message.author)
                    continue

                await msgId.edit(embed=embedVar)
                await reaction.remove(message.author)
                print(page_no)

    if message.content.startswith(botPrefix+"get "):
        if not message.channel.is_nsfw():
            return  # exiting if command isn't in an nsfw channel.

        message_content = message.content.split(' ')
        waifu_name = ""
        embedVar = discord.Embed(
            title="Requested by:"+message.author.display_name, description="Waifu search!", color=0xff6ec7)

        for temp in message_content:

            if (temp != botPrefix+"get"):
                waifu_name = waifu_name+temp+" "

        print(waifu_name)
        channel = message.channel
        waifu_info = searchWaifus(waifu_name)
        waifu_names = []
        waifu_image = []
        waifu_url = []
        waifu_anime = []
        danbooru_images = []
        for waifu in waifu_info:
            waifu_names.append(waifu["name"]["full"])
            waifu_image.append(waifu["image"]["large"])
            waifu_url.append(waifu["siteUrl"])
            waifu_ani = waifu["media"]["nodes"]
            for anime in waifu_ani:
                waifu_anime.append(anime["title"]["userPreferred"])
                # danbooru magic right here.
                danbooru_results = get_from_danbooru(
                    waifu["name"]["full"], anime["title"]["userPreferred"])
                for result in danbooru_results:
                    try:
                        danbooru_images.append(result["large_file_url"])
                        break
                    except:
                        continue

                break

        page_no = 0
        try:
            embedVar = discord.Embed(title="Waifu search!", description="Page "+str(page_no+1)+" of "+str(
                len(waifu_names)), color=0xffabc7).set_thumbnail(url=danbooru_images[page_no])
        except:
            embedVar = discord.Embed(title="Waifu search!", description="Page "+str(
                page_no+1)+" of "+str(len(waifu_names)), color=0xffabc7)
        embedVar.add_field(
            name="Name: ", value=waifu_names[page_no], inline=False)
        embedVar.add_field(name="Anime name:", value=waifu_anime[page_no])
        embedVar.add_field(name="AniList URL:",
                           value=waifu_url[page_no], inline=False)
        msgId = await channel.send(embed=embedVar)

        await msgId.add_reaction('⏮')
        await msgId.add_reaction('🟥')
        await msgId.add_reaction('⏭')
        await msgId.add_reaction('💾')

        def check(reaction, user):
            return user == message.author and str(reaction.emoji) in ['⏮', '⏭', '🟥', '💾']
        while True:
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await msgId.delete()
                break
            else:
                if (reaction.emoji == '⏭' and page_no <= len(waifu_names)-1):
                    page_no += 1

                elif(reaction.emoji == '⏮' and page_no >= 0):
                    page_no -= 1

                elif(reaction.emoji == '💾'):
                    await message.channel.send(embed=embedVar)

                elif(reaction.emoji == '🟥'):
                    await msgId.delete()
                    return

                try:
                    try:
                        embedVar = discord.Embed(title="Waifu search!", description="Page "+str(page_no+1)+" of "+str(
                            len(waifu_names)), color=0xffabc7).set_thumbnail(url=danbooru_images[page_no])
                    except:
                        embedVar = discord.Embed(title="Waifu search!", description="Page "+str(
                            page_no+1)+" of "+str(len(waifu_names)), color=0xffabc7)

                    embedVar.add_field(
                        name="Name: ", value=waifu_names[page_no], inline=False)
                    embedVar.add_field(name="Anime name:",
                                       value=waifu_anime[page_no])
                    embedVar.add_field(name="AniList URL:",
                                       value=waifu_url[page_no], inline=False)
                except:
                    await reaction.remove(message.author)
                    continue

                await msgId.edit(embed=embedVar)
                await reaction.remove(message.author)
                print(page_no)

    if "nigg" in message.content.lower():
        embedVar = discord.Embed(title="OMG "+message.author.display_name+" said the n-word!",
                                 description="By: "+message.author.display_name, color=0xabcdef)

    if message.content.startswith(botPrefix+"danbooru "):
        channel = message.channel
        if not message.channel.is_nsfw():
            return

        tag = message.content.split(' ')[1]
        print(tag)
        page_no = 0
        # getting posts for given tag
        posts = get_from_danbooru_by_tag(tag)
        images = []

        for x in posts:
            try:
                images.append(x["large_file_url"])
            except:
                continue
        # got the images. Now what? Embeds!

        try:
            embedVar = discord.Embed(title="Danbooru results!", description="Page "+str(
                page_no+1)+" of "+str(len(images)), color=0xffabc7).set_image(url=images[page_no])
        except:
            embedVar = discord.Embed(title="Danbooru results!", description="Page "+str(
                page_no+1)+" of "+str(len(images)), color=0xffabc7)

        msgId = await channel.send(embed=embedVar)

        await msgId.add_reaction('⏮')
        await msgId.add_reaction('🟥')
        await msgId.add_reaction('⏭')
        await msgId.add_reaction('💾')

        def check(reaction, user):
            return user == message.author and str(reaction.emoji) in ['⏮', '⏭', '🟥', '💾']

        while True:
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await msgId.delete()
                break
            else:
                if (reaction.emoji == '⏭' and page_no <= len(images)-1):
                    page_no += 1

                elif(reaction.emoji == '⏮' and page_no >= 0):
                    page_no -= 1

                elif(reaction.emoji == '🟥'):
                    await msgId.delete()
                    return

                elif(reaction.emoji == '💾'):
                    await message.channel.send(embed=embedVar)

                try:
                    try:
                        embedVar = discord.Embed(title="Danbooru results!", description="Page "+str(
                            page_no+1)+" of "+str(len(images)), color=0xffabc7).set_image(url=images[page_no])
                    except:
                        embedVar = discord.Embed(title="Danbooru results!", description="Page "+str(
                            page_no+1)+" of "+str(len(images)), color=0xffabc7)
                except:
                    await reaction.remove(message.author)
                    continue

                await msgId.edit(embed=embedVar)
                await reaction.remove(message.author)
                print(page_no)
    
    if message.content.startswith(botPrefix+"digit "):
        channel = message.channel
        if not channel.is_nsfw():
            return

        digit = message.content.split(' ')[1]
        for x in {'nhentai', '9hentai', 'nyahentai'}:
            embedVar = discord.Embed(title = x, description=print_info(digit, x))
            await channel.send(embed=embedVar)
        
        return
        


    # Waifu Stuffs Here onwards.
    if message.content.startswith(botPrefixW+"roll"):
        waifu_info = generate_random_waifu()
        embedVar = discord.Embed(title="Waifu roll!", description="Use 🎲 to roll, 💘 to catch.").set_author(
            name=message.author).set_thumbnail(url=message.author.avatar_url)
        msgId = await message.channel.send(embed=embedVar)
        await msgId.add_reaction('🎲')
        await msgId.add_reaction('💘')
        await msgId.add_reaction('🟥')

        def check(reaction, user):
            return user == message.author and str(reaction.emoji) in ['🎲', '💘', '🟥']

        while True:
            embedVar = discord.Embed(title="Waifu roll!", description="Use 🎲 to roll, 💘 to catch.").set_author(
                name=message.author).set_thumbnail(url=message.author.avatar_url)
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await msgId.delete()
                break
            else:
                embedVar = discord.Embed(title="Waifu roll!", description="Use 🎲 to roll, 💘 to catch.").set_author(
                    name=message.author).set_thumbnail(url=message.author.avatar_url)
                if (reaction.emoji == '🎲'):
                    waifu_info = generate_random_waifu()
                    try:
                        embedVar.set_thumbnail(url=waifu_info["image"]["large"]).add_field(
                            name=waifu_info["name"]["full"], value=waifu_info["media"]["nodes"][0]["title"]["userPreferred"])
                    except:
                        anime = ""
                        for x in waifu_info["media"]["nodes"]:
                            if len(x) != 0:
                                anime = x
                                break
                        embedVar.set_thumbnail(url=waifu_info["image"]["large"]).add_field(
                            name=waifu_info["name"]["full"], value=anime)

                elif (reaction.emoji == '💘'):
                    await msgId.delete()
                    await message.channel.send("💘 **"+message.author.display_name+"** claimed **"+waifu_info["name"]["full"]+"**.")
                    return
                elif (reaction.emoji == '🟥'):
                    await msgId.delete()
                    return

                try:
                    await msgId.edit(embed=embedVar)
                except:
                    await reaction.remove(message.author)
                    continue
                await reaction.remove(message.author)

    try:
        await message.channel.send(embed=embedVar)
    except:
        return

client.run('API_KEY_HERE')
