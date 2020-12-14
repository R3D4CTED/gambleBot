from databaseUtils import *
from anilistTest import *
import discord
from pybooru import Danbooru
import requests
import random
from saucenao_api import SauceNao

def get_waifus(blacklist: list=[]) -> dict:
    """OPTIONAL: blacklist are URL's to not be received."""
    
    #getting 30 waifus from waifu.pics
    URL="https://waifu.pics/api/many/sfw/waifu"
    json = {
            "files": blacklist
        }
    response=requests.post(url=URL, json=json)
    return response.json()

def get_xwaifus(blacklist: list=[]) -> dict:
    """OPTIONAL: blacklist are URL's to not be received."""
    
    #getting 30 nsfw waifus from waifu.pics
    URL="https://waifu.pics/api/many/nsfw/waifu"
    json = {
            "files": blacklist
        }
    response=requests.post(url=URL, json=json)
    return response.json()

def get_waifu():
    #getting 1 waifu from waifu.pics
    URL = "https://waifu.pics/api/sfw/waifu"
    response = requests.get(url=URL)
    return response.json()['url']

def get_xwaifu():
    #getting 1 nsfw waifu from waifu.pics
    URL = "https://waifu.pics/api/nsfw/waifu"
    response = requests.get(url=URL)
    print (response.json()['url'])
    return response.json()['url']

def get_neko():
    #getting a neko from nekos.life
    URL = "https://nekos.life/api/neko"
    response = requests.get(url=URL)
    return response.json()['neko']

def get_from_danbooru_by_tag(tag):
    client = Danbooru('danbooru')
    tags = client.tag_list(name_matches=tag, hide_empty="yes", order="count")
    tag = ""
    for x in tags:
        if len(x)!=0:
            #making sure that the particular tag isn't empty. If it is, then a random image is displayed.
            tag = x["name"]
            break
    
    #got the tags. Now what? Images!

    posts = client.post_list(tags=tag, random=True, raw=True)
    return posts
    



def get_from_danbooru(char_name, anime_name):
    full_tag = char_name + " ("+anime_name+")"
    #print(full_tag)
    client = Danbooru('danbooru')
    #getting full tag AKA Character_Nme(Anime Name) format
    tags = client.tag_list(name_matches=full_tag, hide_empty="yes", order="count")
    print(tags)
    tag = ""
    #Checking if there were no search results, and then getting tags with merely the character name
    if(len(tags)==0):
        tags = client.tag_list(name_matches=char_name, hide_empty="yes", order="count")
    
    if(len(tags)==0):
        #searching for last name, first name format, if the other doesn't work
        reverse_name = ""
        name = char_name.split(' ')
        n = len(name) - 1
        while(n>=0):
            reverse_name = reverse_name+" "+name[n]
            n-=1
        
        print(reverse_name)
        
        tags = client.tag_list(name_matches=reverse_name, hide_empty="yes", order="count")


    
    for x in tags:
        if len(x) != 0:
            tag=x["name"]
            break
    print(tag)

    #get posts for tag.
    posts=client.post_list(tags=tag, random=True, raw=True)
    #print(posts[0]['large_file_url'])
    return posts

def generate_random_waifu():
    tier_list = ['S']*100 + ['A']*500 + ['B']*1000 + ['C']*1500 + ['D']*1900 #can be modded to change probabilities.
    tier = random.choice(tier_list)
    choice = {
        'S': {
            "start" : 1,
            "end" : 100
        },
        'A': {
            "start" : 101,
            "end" : 600
        },
        'B': {
            "start" : 601,
            "end" : 1600
        },
        'C': {
            "start" : 1601,
            "end" : 3100
        },
        'D': {
            "start" : 3101,
            "end" : 5000
        }
    }.get(tier)
    n = random.randint(choice["start"], choice["end"])
    
    
    
    #no need to change the code below.
    waifu_info = get_waifuinfo_id(n)
    insert_waifu_pos_data(waifu_info["id"], n)
    waifu_id = waifu_info["id"]
    print(f"ID:{waifu_id}. Position:{n}")
    return waifu_info

def get_sauce(url):
    sauce = SauceNao()
    return sauce.from_url(url)[0]    

    """
    for post in posts:
        try:
            print(post['large_file_url'])
            break
        except:
            continue

    return posts
    """

