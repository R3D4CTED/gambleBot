from bs4 import BeautifulSoup
import requests

def print_info(page_id: int, site: str):
    try:
        data = soupify(fetch_website(manga(page_id, site))).find(id='tags').text
    except AttributeError:
        return (f"Requested manga not found on {site}. \n")

    no_digits = ""
    for x in data:
        if not x.isdigit():
            if x == 'K':
                no_digits = no_digits+", "
            else:
                no_digits = no_digits+x

    return (f'{site}\nYour url: {manga(page_id, site)}\n{no_digits}\n')

def manga(page: int, source: str):
    """Returns the correct URL for the given source"""
    if source == 'nhentai':
        return f"https://nhentai.net/g/{page}"
    elif source == '9hentai':
        return f"https://9hentai.com/g/{page}"
    elif source == 'nyahentai':
        return f"https://nyahentai.com/g/{page}"

def fetch_website(url: str):
    """Loading website and returning the HTML"""
    return requests.get(url).text

def soupify(soup):
    """Parses HTML into readable format via BeautifulSoup"""
    return BeautifulSoup(soup, 'html.parser')
