import pymongo

#Remote declarations.
client = pymongo.MongoClient("mongodb://localhost:27017/")
print(client.list_database_names())
waifudb = client['waifu']
userdb = waifudb['user_data']
waifu_datadb = waifudb['waifu_data_db']
roll_statsdb = waifudb['roll_stats']

def waifu_roll_in_progress(user_id, is_in_progress):
    insertion = {
        "user_id" : user_id,
        "is_in_progress" : is_in_progress
    }
    
    #checking if the entry for the user already exists on DB
    if (len(list(roll_statsdb.find({"user_id" : user_id}))) == 0):
        roll_statsdb.insert_one(insertion)
    
    #otherwise, just finding and replacing
    else:
        roll_statsdb.find_one_and_replace({"user_id" : user_id}, insertion)
    
def is_waifu_roll_in_progress(user_id):
    query = {
        "user_id" : user_id
    }
    try:
        return roll_statsdb.find_one(query)["is_in_progress"]
    except:
        return False

def list_hentai():
    hentaidb = waifudb['hentaidigits']
    for x in hentaidb.find():
        print(x)

def insert_hentai(n):
    insertion = {"id" : n}
    hentaidb = waifudb['hentaidigits']
    hentaidb.insert_one(insertion)

def claim_waifu(user_id, anilist_id):
    insertion = {
        "user_id" : user_id,
        "anilist_id" : anilist_id
    }
    userdb.insert_one(insertion)

def get_waifu_list_for_user(user_id):
    query = {
        'user_id' : user_id
    }
    return list(userdb.find(query))

def insert_waifu_data_into_db(anilist_id, name, image_url, anime_name):
    insertion = {
        'anilist_id' : anilist_id,
        'name' : name,
        'anime_name' : anime_name,
        'image_url' : image_url
    }
    waifu_datadb.insert_one(insertion)

def get_waifu_data_from_db(anilist_id):
    query = {
        'anilist_id' : anilist_id
    }
    return waifu_datadb.find_one(query)
