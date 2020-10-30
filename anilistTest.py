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
