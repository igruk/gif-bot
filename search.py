import os
import json
from typing import Dict, List

import requests
from dotenv import load_dotenv

load_dotenv()

SUBSCRIPTION_KEY = os.getenv('SUBSCRIPTION_KEY')
HEADERS = {'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY}
WEB_SEARCH_URL = 'https://api.bing.microsoft.com/v7.0/search'
VISUAL_SEARCH_URL = 'https://api.bing.microsoft.com/v7.0/images/visualsearch'


def print_json(obj: Dict) -> None:
    """Print object as json"""
    print(json.dumps(obj, sort_keys=True, indent=2, separators=(',', ': ')))


def remove_words_from_string(text: str) -> str:
    """Remove needless words from text"""
    needless_words = ('tenor', 'pinterest', 'gif', 'gifs')
    text_list = text.split()
    filtered_words = [word for word in text_list if word not in needless_words]
    return ' '.join(filtered_words)


def get_list_of_results(data: Dict) -> List[str]:
    """Return list of search results"""
    results = []
    hosts = ('Tenor', 'Pinterest')
    content_url = 'https://tenor.com/'
    host_name = 'hostPageDomainFriendlyName'
    host_url = 'hostPageUrl'

    try:
        objects = data['tags'][0]['actions']
    except KeyError as e:
        print(e)
        return results

    for obj in objects:
        try:
            items = obj['data']['value']
        except KeyError:
            continue

        for item in items:
            if (host_name in item and item[host_name] in hosts) \
                    or (host_url in item and item[host_url].startswith(content_url)):
                results.append(item['name'].lower())
        if results:
            return results

    return results


def search_results_to_queries(results: List[str]) -> List[str]:
    """Get visual search results and transform them into queries for web search"""
    know_your_meme = ' know your meme'
    queries = []
    for result in results:
        query = result.split('-')[0]
        query = remove_words_from_string(query) + know_your_meme
        queries.append(query)
    return queries


def get_meme_url(data: Dict) -> List[str]:
    """Return list of relevant URLs"""
    result = []
    domain_url = 'https://knowyourmeme.com/memes'
    filter_urls = ('https://knowyourmeme.com/memes/subcultures',
                   'https://knowyourmeme.com/memes/people',
                   'https://knowyourmeme.com/memes/events',
                   'https://knowyourmeme.com/memes/cultures',
                   'https://knowyourmeme.com/memes/sites')

    items = data['webPages']['value']

    for item in items:
        url = item['url'].rstrip('/')
        if url.startswith(domain_url) \
                and not url.startswith(filter_urls) \
                and url.count('/') == 4:
            result.append(url)
    return result


def visual_search(list_frames: List[str]) -> List[str]:
    """Visual search using Bing API"""
    if not list_frames:
        return list_frames

    image_path = list_frames[0]
    file = {'image': ('my_file', open(image_path, 'rb'))}
    response = requests.post(VISUAL_SEARCH_URL, headers=HEADERS, files=file)
    response.raise_for_status()
    json_data = response.json()

    search_results = get_list_of_results(json_data)
    ready_queries = search_results_to_queries(search_results)

    return ready_queries


def web_search(list_queries: List[str]) -> List[str]:
    """Web search using Bing API"""
    if not list_queries:
        return list_queries

    search_term = list_queries[0]
    params = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}
    response = requests.get(WEB_SEARCH_URL, headers=HEADERS, params=params)
    response.raise_for_status()
    json_data = response.json()

    search_results = get_meme_url(json_data)

    return search_results
