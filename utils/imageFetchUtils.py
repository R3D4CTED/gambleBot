import random
import requests
from pybooru import Danbooru


def get_waifus(blacklist: list=[], lewd: str="sfw") -> dict:
    """OPTIONAL: blacklist are URL's to not be received."""
    
    #getting 30 waifus from waifu.pics
    URL=f"https://waifu.pics/api/many/{lewd}/waifu"
    json = {
            "files": blacklist
        }
    response=requests.post(url=URL, json=json)
    return response.json()

def get_nekos(blacklist: list=[], lewd: str="sfw") -> dict:
    """OPTIONAL: blacklist are URL's to not be received."""
    
    #getting 30 waifus from waifu.pics
    URL=f"https://waifu.pics/api/many/{lewd}/nekos"
    json = {
            "files": blacklist
        }
    response=requests.post(url=URL, json=json)
    return response.json()


def get_waifu(lewd: str="sfw"):
    #getting 1 waifu from waifu.pics
    URL = f"https://waifu.pics/api/{lewd}/waifu"
    response = requests.get(url=URL)
    return response.json()['url']

def get_neko():
    #getting a neko from nekos.life
    url_nekos_life = "https://nekos.life/api/v2/img/neko"
    url_waifu_pics = "https://waifu.pics/api/sfw/neko"
    response_nekos_life = requests.get(url=url_nekos_life).json()['url']
    response_waifu_pics = requests.get(url=url_waifu_pics).json()['url']
    return random.choice([response_nekos_life, response_waifu_pics])

def get_xneko():
    #getting a lewd neko from nekos.life
    #getting a neko from nekos.life
    url_nekos_life = "https://nekos.life/api/v2/img/lewd"
    url_waifu_pics = "https://waifu.pics/api/nsfw/neko"
    response_nekos_life = requests.get(url=url_nekos_life).json()['url']
    response_waifu_pics = requests.get(url=url_waifu_pics).json()['url']
    return random.choice([response_nekos_life, response_waifu_pics])


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
