from databaseUtils import *
from anilistTest import *
import discord
from pybooru import Danbooru
import requests
import random
from saucenao_api import SauceNao


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

