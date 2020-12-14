#imports
from typing import List
import discord
from discord.ext import commands
import random
import requests
import time
import asyncio
from waifuUtils import *
from anilistTest import *
from nhscript import *
from databaseUtils import *

description = "Bot written for gambling games, weebs and administration."
presence_name = "with [REDACTED]." #defines presence playing with X
token = API_KEY_HERE #enter your bot API key here.

intents = discord.Intents.default()

bot = commands.Bot(command_prefix='*', description=description, intents=intents)
#bot.remove_command('help')
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name=presence_name))

"""
@bot.command(description="Returns help.")
async def help(ctx):
    embedVar = discord.Embed(title="Command list.").set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    for command in bot.commands:
        embedVar.add_field(name=command)
    await ctx.send(embedVar)
    #todo:improve the help command
"""

@bot.command(description="Returns latency.")
async def ping(ctx):
    await ctx.send(f"🏓 Pong ~. Latency is {round(bot.latency*1000)}ms.")

@bot.command(description="Generates a random number between 0 and given number.")
async def rand(ctx, n: float):
    r_n = random.randrange(0, round(abs(n)))
    print(ctx.author.mention)
    embedVar = discord.Embed(title="Random number!", description=f"{r_n}", color=0x00ff00).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embedVar)

@bot.command(description="Generates random waifu image.")
async def waifu(ctx):
    waifu_url = get_waifu()
    print("Waifu Image URL:"+waifu_url)
    embedVar = discord.Embed(
            title="Waifu!", color=0x00ffcc).set_image(url=waifu_url).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embedVar)
    
@bot.command(description="Generates random Nekomimi. *Nyaa ~*")
async def neko(ctx):
    neko_url = get_neko()
    print(neko_url)
    embedVar = discord.Embed(
        title="Nekos!", description="Nyaa ~", color=0xccff00).set_image(url=neko_url).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embedVar)

@bot.command(description="Gets NSFW waifu image.")
async def xwaifu(ctx):
    if not ctx.channel.is_nsfw():
        await ctx.send("❌ This command can only be run in an NSFW channel.")
        return
    xwaifu_url = get_xwaifu()
    print(xwaifu_url)
    embedVar = discord.Embed(
        title="NSFW Waifu!", color=0x00aacc).set_image(url=xwaifu_url).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    
    await ctx.send(embed=embedVar)

@bot.command(description="Generates waifu images!")
async def images(ctx):
    waifus = get_waifus()["files"]
    waifuList = []
    n = 1
    page_no = 1
    embedVar = discord.Embed(
        title="Waifus!", color=0xfac105).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    msgId = await ctx.send(embed=embedVar)
    
    await msgId.add_reaction('⏮')
    await msgId.add_reaction('🟥')
    await msgId.add_reaction('⏭')
    await msgId.add_reaction('💾')
    
    for x in waifus:
        print(x)
        waifuList.append(x)
        n += 1

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ['⏮', '⏭', '🟥', '💾']
    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
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
                await ctx.send(embed=embedVar)
            
            elif(reaction.emoji == '🟥'):
                await msgId.delete()
                return
            await reaction.remove(ctx.author)
            print(page_no)

@bot.command(description="Generate NSFW Waifu images.")
async def ximages(ctx):
    if not ctx.channel.is_nsfw():
        await ctx.send("❌ This command can only be run in an NSFW channel.")
        return
    
    waifus = get_xwaifus()["files"]
    waifuList = []
    n = 1
    page_no = 1
    embedVar = discord.Embed(
        title="NSFW Waifus!", color=0xfac105).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    msgId = await ctx.send(embed=embedVar)
    await msgId.add_reaction('⏮')
    await msgId.add_reaction('🟥')
    await msgId.add_reaction('⏭')
    await msgId.add_reaction('💾')
    
    for x in waifus:
        waifuList.append(x)
        print(x)
        n += 1

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ['⏮', '⏭', '🟥', '💾']
    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
        
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
                await ctx.send(embed=embedVar)
            
            elif(reaction.emoji == '🟥'):
                await msgId.delete()
                return
            
            await reaction.remove(ctx.author)
            print(page_no)

@bot.command(description="Finds information about given waifu.")
async def find(ctx, waifu_name: str):
    print(waifu_name)
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
    embedVar = discord.Embed(title="Waifu search!",
                                color=0xffabc7).set_image(url=waifu_image[page_no]).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    
    embedVar.add_field(
        name="Name: ", value=waifu_names[page_no], inline=False)
    embedVar.add_field(name="Anime name:", value=waifu_anime[page_no])
    embedVar.add_field(name="AniList URL:",
                        value=waifu_url[page_no], inline=False)
    msgId = await ctx.send(embed=embedVar)

    await msgId.add_reaction('⏮')
    await msgId.add_reaction('🟥')
    await msgId.add_reaction('⏭')
    await msgId.add_reaction('💾')

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ['⏮', '⏭', '🟥', '💾']
    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await msgId.delete()
            break
        else:
            if (reaction.emoji == '⏭' and page_no <= len(waifu_name)-1):
                page_no += 1

            elif(reaction.emoji == '⏮' and page_no >= 0):
                page_no -= 1

            elif(reaction.emoji == '💾'):
                await ctx.send(embed=embedVar)

            elif(reaction.emoji == '🟥'):
                await msgId.delete()
                return

            try:
                embedVar = discord.Embed(title="Waifu search!",
                                            color=0xffabc7).set_image(url=waifu_image[page_no]).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                embedVar.add_field(
                    name="Name: ", value=waifu_names[page_no], inline=False)
                embedVar.add_field(name="Anime name:",
                                    value=waifu_anime[page_no])
                embedVar.add_field(name="AniList URL:",
                                    value=waifu_url[page_no], inline=False)
            except:
                await reaction.remove(ctx.author)
                continue

            await msgId.edit(embed=embedVar)
            await reaction.remove(ctx.author)
            print(page_no)

@bot.command(description="Gets image from Danbooru for given tag.")
async def danbooru(ctx, tag: str):
    if not ctx.channel.is_nsfw():
        await ctx.send("❌ This command can only be run in an NSFW channel.")
        return
    
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
            page_no+1)+" of "+str(len(images)), color=0xffabc7).set_image(url=images[page_no]).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    except:
        embedVar = discord.Embed(title="Danbooru results!", description="Page "+str(
            page_no+1)+" of "+str(len(images)), color=0xffabc7).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

    msgId = await ctx.send(embed=embedVar)

    await msgId.add_reaction('⏮')
    await msgId.add_reaction('🟥')
    await msgId.add_reaction('⏭')
    await msgId.add_reaction('💾')

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ['⏮', '⏭', '🟥', '💾']

    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
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
                await ctx.send(embed=embedVar)

            try:
                try:
                    embedVar = discord.Embed(title="Danbooru results!", description="Page "+str(
                        page_no+1)+" of "+str(len(images)), color=0xffabc7).set_image(url=images[page_no]).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                except:
                    embedVar = discord.Embed(title="Danbooru results!", description="Page "+str(
                        page_no+1)+" of "+str(len(images)), color=0xffabc7).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            except:
                await reaction.remove(ctx.author)
                continue

            await msgId.edit(embed=embedVar)
            await reaction.remove(ctx.author)
            print(page_no)

@bot.command(description="Gets Hentai tags for digits.")
async def digits(ctx, digit: str):
    if not ctx.channel.is_nsfw():
        await ctx.send("❌ This command can only be run in an NSFW channel.")
        return

    if digit.isnumeric():
        try:
            insert_hentai(str(digit))
        except:
            print("Insertion failed. ID was:"+digit)
    
        for x in {'nhentai', '9hentai', 'nyahentai'}:
            embedVar = discord.Embed(title=x, description=print_info(digit, x)).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embedVar)

@bot.command(description="Gets sauce for image URL.")
async def sauce(ctx, url : str):
    result = get_sauce(url)
    try:
        embedVar = discord.Embed(title="Sauce found!", description=f"Given image URL:[Link]({url})", color=0xAB53FF).set_author(name=ctx.author, icon_url=ctx.author.avatar_url).set_thumbnail(url=result.thumbnail)
        embedVar.add_field(name="Title:", value=f"{result.title}", inline=True)
        embedVar.add_field(name="Author:", value=f"{result.author}", inline=True)
        embedVar.add_field(name="Similarity:", value=f"{result.similarity}%", inline=False)
        embedVar.add_field(name="Results:", value=f"[Link]({result.urls[0]})", inline=False)
        embedVar.set_footer(text="Image search provided by SauceNao.")
    except:
        await ctx.send("❌ Not found. Try on IQDB.")
        return
    
    await ctx.send(embed=embedVar)


@bot.group(description="Waifu Roulette Commands Group.")
async def w(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("❌ That is not a valid waifu roulette command!")
    
@w.command(name="roll")
async def _roll(ctx):
    user_id = ctx.author.id
    roll_limit = 10
    n = 0
    if(is_waifu_roll_in_progress(user_id)):
        await ctx.channel.send(f"❌ **{ctx.author.display_name}**, you already have a waifu roulette session in progress.")
        return

    else:
        waifu_roll_in_progress(user_id, True)
    
    if(is_rate_limited(user_id)):
        await ctx.channel.send(f"❌**{ctx.author.display_name}**, you are rolling too much. Try again in {get_time_left(user_id)} seconds.")
        waifu_roll_in_progress(user_id, False)
        return
    
    else:
        set_roll_rate_limit(user_id)

    try:
        waifu_info = generate_random_waifu()
    except:
        await ctx.send(f"❗ {ctx.author.display_name}, we seem to be experiencing issues. Try again after some time. Admin has been notified.")
        waifu_roll_in_progress(user_id, False)
        return

    
    embedVar = discord.Embed(title="Waifu roll!", description="Use 🎲 to roll, 💘 to claim.").set_author(
        name=ctx.author, icon_url=ctx.author.avatar_url).set_image(url=ctx.author.avatar_url)
    msgId = await ctx.send(embed=embedVar)
    
    await msgId.add_reaction('🎲')
    await msgId.add_reaction('💘')
    await msgId.add_reaction('🟥')

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ['🎲', '💘', '🟥']

    while True:
        embedVar = discord.Embed(title="Waifu roll!", description="Use 🎲 to roll, 💘 to claim.").set_author(
            name=ctx.author, icon_url=ctx.author.avatar_url).set_image(url=ctx.author.avatar_url)
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await msgId.delete()
            waifu_roll_in_progress(user_id, False)
            return

        else:
            embedVar = discord.Embed(title="Waifu roll!", description="Use 🎲 to roll, 💘 to claim.").set_author(
                name=ctx.author, icon_url=ctx.author.avatar_url).set_image(url=ctx.author.avatar_url)

            if (reaction.emoji == '🎲'):
                if (n>roll_limit):
                    await ctx.send(f"❌**{ctx.author.display_name}**, {roll_limit} rolls per turn only.")
                    await reaction.remove(ctx.author)
                    continue
                waifu_info = generate_random_waifu()
                n += 1
                try:
                    embedVar.set_image(url=waifu_info["image"]["large"]).add_field(
                        name=waifu_info["name"]["full"], value=waifu_info["media"]["nodes"][0]["title"]["userPreferred"])
                except:
                    await msgId.delete()
                    await ctx.send(f"{ctx.author.mention}, sincere apologies, we seem to have encountered an error. Admin notified.")
                    waifu_roll_in_progress(user_id, False)

            elif (reaction.emoji == '💘'):
                await msgId.delete()
                waifu_roll_in_progress(user_id, False)
                await ctx.send("💘 **"+ctx.author.display_name+"** claimed **"+waifu_info["name"]["full"]+"**.")
                try:
                    claim_waifu(user_id, waifu_info["id"])
                    insert_waifu_data_into_db(waifu_info["id"], waifu_info["name"]["full"], waifu_info["image"]
                                                ["large"], waifu_info["media"]["nodes"][0]["title"]["userPreferred"])
                except:
                    await ctx.send("Something went wrong, your request has been saved and will be processed soon.")

                return
            elif (reaction.emoji == '🟥'):
                await msgId.delete()
                waifu_roll_in_progress(user_id, False)
                return

            try:
                await msgId.edit(embed=embedVar)
            except:
                await reaction.remove(ctx.author)
                continue
            await reaction.remove(ctx.author)

@w.command(name="list")
async def _list(ctx):
    user_id = ctx.author.id
    waifu_ids = get_waifu_list_for_user(user_id)
    if len(waifu_ids) == 0:
        await ctx.send(f"❌You seem to not have claimed any waifus. Use ``{bot.command_prefix}w roll`` to claim a waifu and try again.")
        return
    page_no = 0
    embedVar = discord.Embed(title=get_waifu_data_from_db(waifu_ids[page_no]["anilist_id"])["name"], description=get_waifu_data_from_db(waifu_ids[page_no]["anilist_id"])["anime_name"]).set_author(
        icon_url=ctx.author.avatar_url, name=ctx.author).set_image(url=get_waifu_data_from_db(waifu_ids[page_no]["anilist_id"])["image_url"]).set_footer(text=f"{bot.command_prefix}roulette roll to claim.")
    msgId = await ctx.send(embed=embedVar)
    
    await msgId.add_reaction('⏮')
    await msgId.add_reaction('🟥')
    await msgId.add_reaction('⏭')
    await msgId.add_reaction('💔')
    await msgId.add_reaction('💾')

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ['⏮', '⏭', '🟥', '💾', '💔']

    while True:
        embedVar = discord.Embed(title=get_waifu_data_from_db(waifu_ids[page_no]["anilist_id"])["name"], description=get_waifu_data_from_db(waifu_ids[page_no]["anilist_id"])["anime_name"]).set_author(
            icon_url=ctx.author.avatar_url, name=ctx.author).set_image(url=get_waifu_data_from_db(waifu_ids[page_no]["anilist_id"])["image_url"]).set_footer(text=f"{bot.command_prefix}roulette roll to claim.")
        
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await msgId.delete()
            return
        
        else:
            if(reaction.emoji == '⏮' and page_no>=0):
                page_no -= 1
            
            elif (reaction.emoji == '⏭' and page_no<=len(waifu_ids)-1):
                page_no+= 1
            
            elif(reaction.emoji == '🟥'):
                await msgId.delete()
                return
            
            if (page_no<0):
                page_no = 0
            
            elif (page_no>len(waifu_ids)-1):
                page_no = len(waifu_ids)-1
            
            embedVar = discord.Embed(title=get_waifu_data_from_db(waifu_ids[page_no]["anilist_id"])["name"], description=get_waifu_data_from_db(waifu_ids[page_no]["anilist_id"])["anime_name"]).set_author(
                icon_url=ctx.author.avatar_url, name=ctx.author).set_image(url=get_waifu_data_from_db(waifu_ids[page_no]["anilist_id"])["image_url"]).set_footer(text=f"{bot.command_prefix}roulette roll to claim.")
            
            if(reaction.emoji == '💾'):
                await ctx.send(embed=embedVar)
                await reaction.remove(ctx.author)
                continue

            if (reaction.emoji == '💔'):
                try:
                    remove_waifu(ctx.author.id, waifu_ids[page_no]["anilist_id"])
                except:
                    await ctx.send("An error occurred. Please try again.")
                    await msgId.delete()

                waifu_name = get_waifu_data_from_db(waifu_ids[page_no]["anilist_id"])["name"]
                await ctx.send(f"<@!{ctx.author.id}> dumped **{waifu_name}**.")
                await msgId.delete()
                return
            
            await msgId.edit(embed=embedVar)
            await reaction.remove(ctx.author)


@commands.is_owner()
@bot.group(description="Admin commands.")
async def admin(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("❌ Baka Admin! Go learn the commands first!")

@admin.command(name="info")
async def _info(ctx):
    await ctx.send(f"Admin senpai is **{ctx.author.display_name}**.")

@admin.command(name="restartroulette")
async def _restart(ctx):
    msgId = await ctx.send(f"{ctx.author.mention} Resetting...")
    try:
        reset_user_roll_stats()
        await msgId.edit(content="Reset.")
    except:
        await msgId.edit(content="Resetting DB failed.")

@admin.command(name="addwaifu")
async def _addwaifu(ctx, user_id : int, waifu_id : int):
    try:
        print(user_id)
        claim_waifu(user_id, waifu_id)
        waifu_data = get_waifu_info_for_id(waifu_id)
        print(waifu_data["name"]["full"])
        insert_waifu_data_into_db(waifu_id, waifu_data["name"]["full"], waifu_data["image"]["large"], waifu_data["media"]["nodes"][0]["title"]["userPreferred"])
    except:
        await ctx.send(f"{ctx.author.mention} Failed to add waifu. Check logs.")
        return
    waifu_name = waifu_data["name"]["full"]
    await ctx.send(f"{ctx.author.mention}, **{waifu_name}** has been added to <@!{user_id}>\'s harem.")

@admin.command(name="removewaifu")
async def _removewaifu(ctx, user_id : int, waifu_id : int):
    try:
        print(user_id)
        remove_waifu(user_id, waifu_id)
    except:
        await ctx.send(f"{ctx.author.mention}, removing waifu with id {waifu_id} from <@!{user_id}> failed.")
        return
    
    await ctx.send(f"{ctx.author.mention}, removing waifu with id {waifu_id} from <@!{user_id}> was successful.")


bot.run(token)

