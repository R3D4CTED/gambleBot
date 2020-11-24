import requests

def searchWaifu(search_term):
    URL = 'https://graphql.anilist.co'
    query = '''
    query ($term: String) {
        Character(search: $term) {
            id
        }
    }
    '''
    variables = {
        'term': search_term
    }

    response = requests.post(
        URL, json={'query': query, 'variables': variables})
    id = response.json()["data"]["Character"]["id"]
    query = '''
    query($id: Int) {
        Character(id: $id) {
            name {
                full
                native
            }
            image {
                large
            }
            description(asHtml:false)
            siteUrl
        }
    }
    '''
    variables = {
        'id': id
    }

    response = requests.post(
        URL, json={'query': query, 'variables': variables})
    return response.json()["data"]["Character"]


def searchWaifus(search_term):
    URL = 'https://graphql.anilist.co'
    query = '''
    query($term: String) {
        Page(perPage: 10) {
            characters(search: $term) {
                siteUrl
                image {
                    large
                }
                name {
                    full
                    native
                }
                media(sort:ID, type:ANIME, page:1, perPage: 1) {
                    nodes {
                        title {
                            english
                            userPreferred
                        }
                    }
                }
            }
        }
    }
    '''
    variables = {
        'term': search_term
    }
    response = requests.post(
        URL, json={'query': query, 'variables': variables})
    return response.json()["data"]["Page"]["characters"]


def get_waifuinfo_id(id):
    URL = 'https://graphql.anilist.co'
    print(id)
    query = '''
    query($id: Int) {
        Page(page:$id, perPage:1) {
            characters(sort:FAVOURITES_DESC) {
                id
                siteUrl
                image {
                    large
                }
                name{
                    full
                }
                media(perPage: 1, sort: POPULARITY_DESC) {
			        nodes {
					    title {
				  	        userPreferred
					    }
			        }
                }
            }
        }
    }
    '''
    variables = {
        'id': id
    }

    response = requests.post(
        URL, json={'query': query, 'variables': variables})
    try:
        return response.json()["data"]["Page"]["characters"][0]
    except:
        return
