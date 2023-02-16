import requests
import webbrowser
import urllib
import re
from requests_html import HTML
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from images import is_similar


def get_url_by_photo(filePath):
    '''повертає url адресу гугл пошуку по завантаженому фото'''

    searchUrl = 'http://www.google.com/searchbyimage/upload'
    multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
    response = requests.post(searchUrl, files=multipart, allow_redirects=False)
    fetchUrl = response.headers['Location']
    return fetchUrl


def get_source(url):
    '''повертає html код сторінки за url адресою'''

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)


def get_result(filePath):
    '''повертає результат пошуку по завантаженому фото'''

    fetchUrl = get_url_by_photo(filePath)
    response = get_source(fetchUrl)

    css_identifier_result = ".fKDtNb"

    results = response.html.find(css_identifier_result)
    main_result = results[0].find(css_identifier_result, first=True).text

    return main_result


def get_query(result):
    '''приймає результат пошуку і повертає сформований запит'''

    q = result.lower().replace(' gif ', ' ')
    if q.endswith(' gif'):
        q = q[:-4]
    if q.startswith('gif '):
        q = q[4:]

    query = 'knowyourmeme ' + q

    return q, query


def get_knowyourmeme_url(query):
    '''повертає посилання на статтю knowyourmeme про даний мем. якщо статтю не знайдено - повертає запит'''

    q = query[0].title()

    query = urllib.parse.quote_plus(query[1])
    response = get_source("https://www.google.com/search?q=" + query)

    links = list(response.html.absolute_links)

    filter_domains = ('https://knowyourmeme.com/memes/subcultures',
                      'https://knowyourmeme.com/memes/people',
                      'https://knowyourmeme.com/memes/events',
                      'https://knowyourmeme.com/memes/cultures',
                      'https://knowyourmeme.com/memes/subcultures/'
                      'https://knowyourmeme.com/memes/sites')

    knowyourmeme = 'https://knowyourmeme.com/memes'

    for url in links[:]:
        if not url.startswith(knowyourmeme) or url.startswith(filter_domains):
            links.remove(url)


    links_url = []

    for url in links[:]:
        if url.count('/') == 4:
            if url not in links_url:
                links_url.append(url)
        elif url.count('/') == 5:
            l = len(url.split('/')[-1])
            url = url[:-l-1]
            if url not in links_url:
                links_url.append(url)
    return links_url


def valid_meme(url, list_frames):
    '''перевіряє чи дана стаття дійсно про потрібний мем'''

    if not url.startswith('https://knowyourmeme.com/memes'):
        return True

    page = get_source(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    # image_url = soup.find(class_='photo left wide')
    fave_tag = soup.find(class_='fave')
    image_url = fave_tag.find_next_sibling()
    if image_url:
        image_url = image_url['href']
    else:
        return True

    image_name = image_url[-6:]
    download_image_path = 'downloads/data/' + image_name
    urllib.request.urlretrieve(image_url, download_image_path) # завантаження зображення по url

    for frame in list_frames:
        valid = is_similar(download_image_path, frame, 28)
        if valid:
            return True
    return False


def get_info_about_meme(url):
    '''повертає інформацію про мем за посиланням на knowyourmeme'''

    if not url.startswith('https://knowyourmeme.com/memes'):
        return url

    page = get_source(url)

    found = re.search('About</h2>([\S\s]+)<h2 id="origin', page.text).group(1)

    soup = BeautifulSoup(found, 'html.parser')
    meme = soup.find(name='strong').text
    source = soup.find(name='em')

    if source:
        result = f'{meme} from {source.text}'
    else:
        result = meme

    return result

