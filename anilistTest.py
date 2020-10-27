import requests
import json

def searchWaifu(search_term):
	URL = 'https://graphql.anilist.co'
	query = '''
	query ($term: String) { 
		Character(search: $term) {
	    	id
	  	}
	}
	'''
	variables= {
		'term' : search_term
	}

	response = requests.post(URL, json={'query': query, 'variables': variables})
	id = response.json()["data"]["Character"]["id"]
	query='''
	query($id: Int) {
		Character(id: $id) {
			name {
				full
			}
		}
	}
	'''
	variables= {
		'id' : id
	}

	response = requests.post(URL, json={'query': query, 'variables': variables})
	full_name=response.json()["data"]["Character"]["name"]["full"]
	return full_name
