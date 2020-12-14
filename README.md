# [REDACTED]'s Hentai Slave.
A multifeatured Discord bot written in discord.py mainly aimed at gambling games. Part of a learning experience in making a fully featured bot to administer a major server and provide hours of fun.

## Requirements
```
discord.py
requests
pybooru
bs4
saucenao-api
```
[MongoDB](https://www.mongodb.com/try/download/community).



## Installation
Install dependencies using:
```
pip install -r requirements.txt
```
Make sure you have MongoDB server running on port 27017 and check whether it is accessible before you launch the bot.

Open up slaveBot.py in a text editor and enter the bot access token in the place specified at the end of the file. More details on how to get one at [Discord developer portal](https://discord.com/developers/docs/intro).

After this, you're ready to run it! You can also set bot prefix by changing the value of the variable at the beginning of the script. 


## Credits
[nekos.life](https://nekos.life) and [waifu.pics](https://waifu.pics) for the image API. [Anilist](https://anilist.co/) for the waifu/anime-related API. [Danbooru](https://danbooru.donmai.us/) for the dedicated NSFW image providing.
Respect and greetings to [Snaacky](https://github.com/snaacky), [Stalker](https://github.com/JesseyWhite) and [Subby](https://github.com/callmekory)

### Further thoughts
Working on a waifu roulette with more features than other alternatives and being FOSS all the way!


## Command list
Assuming that "\*" is the command prefix.
```
---GENERAL/SFW---
*ping => Returns latency.
*random N => Returns a random number between 0 and N(if N is negative, it'll be converted to positive)
*waifu => 1 random waifu image from waifu.pics
*neko => 1 random nekomimi image from nekos.life
*images => Batch of waifu images from waifu.pics in a paginator form.
*find "CHARACTER NAME" => Fetches information about a character on AniList.

--GENERAL/NSFW--
*xwaifu => 1 random NSFW waifu image from waifu.pics
*ximages => Batch of NSFW waifu images from waifu.pics in a paginator form.
*danbooru "TAG" => Gets image for given tag from Danbooru. Only one tag supported currently.
*digits DIGIT => Searches nhentai/nyahentai/9hentai for the given hentai ID and returns tags.

--WAIFU ROULETTE--
*w roll => Start the waifu roll. Currently 10/turn, 1 roll/250 seconds due to AniList API restrictions.
*w list => Lists all the waifus you claimed.

--ADMIN COMMANDS(OWNER ONLY}--
NOTE: "OWNER" is the account with which the bot API key was generated.
*admin info => Displays name/tag of Admin.
*admin restartroulette => Resets the rolling time limitations/current rolling status. Use only if an error occurred and bot crashed during execution.
*admin addwaifu USER_ID ANILIST_ID => Adds a waifu to a player. Do not abuse this.
*admin removewaifu USER_ID ANILIST_ID => Removes a waifu from a player. Do not abuse this.
```
