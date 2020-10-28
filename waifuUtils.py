import discord
import requests

def get_waifus(blacklist: list=[]) -> dict:
    """OPTIONAL: blacklist are URL's to not be recieved."""
    
    #getting 30 waifus from waifu.pics
    URL="https://waifu.pics/api/many/sfw/waifu"
    json = {
            "files": blacklist
        }
    response=requests.post(url=URL, json=json)
    return response.json()

def get_waifu():
    #getting 1 waifu from waifu.pics
    URL = "https://waifu.pics/api/sfw/waifu"
    response = requests.get(url=URL)
    print (response.json()['url'])
    return response.json()['url']
