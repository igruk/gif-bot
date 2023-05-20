import re
from typing import List

import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup

from frames import split_video
from search import visual_search, web_search


def get_html(url: str) -> str:
    """Return the HTML code of the page by the given URL"""
    try:
        session = HTMLSession()
        response = session.get(url)
        html = response.text
        return html

    except requests.exceptions.RequestException as e:
        raise e


def get_info_from_knowyourmeme(urls: List[str]) -> str:
    """Return info about the meme by the given URL to knowyourmeme site"""
    if not urls:
        return "Sorry, couldn't find it"

    # Get the HTML code of the page
    url = urls[0]
    html = get_html(url)

    # Extract the meme's name using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    meta_tag = soup.find('meta', {'property': 'og:title'})
    name = meta_tag.get('content') if meta_tag else None

    # Extract the desired information using regular expressions and BeautifulSoup
    pattern = 'About</h2>([\S\s]+)<h2 id="spread'
    match_object = re.search(pattern, html)
    captured_text = match_object.group(1)
    soup = BeautifulSoup(captured_text, 'html.parser')

    meme = name if name else soup.find(name='strong').text
    source = soup.find(name='em').text if soup.find(name='em') else None
    info = f'{meme} from {source}' if source else meme

    return info


def get_info_about_meme(file_path: str) -> str:
    """Find information about the meme"""
    # Split video into frames and get list of non-identical frames
    frames = split_video(file_path)

    # Visual search using Bing API
    visual_search_results = visual_search(frames)

    # Web search using Bing API
    web_search_results = web_search(visual_search_results)

    # Get information about meme using BeautifulSoup
    info = get_info_from_knowyourmeme(web_search_results)

    return info
