import requests as rq
from bs4 import *
import validators
import time
from urllib.parse import urlparse


def get_links(url, level):
    time.sleep(5)
    r = rq.get(url)

    soup = BeautifulSoup(r.text, "html.parser")

    links = {}

    for link in soup.findAll('a'):
        temp_dict = {}
        if (link.get('href') not in links):
            temp_dict[link.get('href')] = [level, link.get('href')]
            links.update(temp_dict)

    return links

def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False

def search_images(url, max_level):
    max_level = int(max_level)
    primary_links = {'links': []}
    primary_links['links'].append([0, url])

    i = 0
    while (i < len(list(primary_links['links']))):
            arr = primary_links['links'][i]
            link = arr[1]
            level = arr[0]
            val = uri_validator(link)
            if val:
                if level < max_level:
                    level += 1
                    links = get_links(link, level)
                    for new_link in links:
                        if new_link not in primary_links['links']:
                            temp_dict = {level, new_link}
                            primary_links['links'].append(list(temp_dict))
            i += 1;

    dict_to_return = {'results': []}

    for level, link in primary_links['links']:
        valid = validators.url(str(link))
        if valid:
            r = rq.get(link)
            soup = BeautifulSoup(r.text, "html.parser")
            images = soup.findAll('img')
            for image in images:
                temp_dict = {'imageUrl': image['src'], 'sourceUrl': link, 'depth': level}
                dict_to_return['results'].append(temp_dict)

    return dict_to_return


if __name__ == '__main__':
    url, depth = input('please enter url and depth seperated by space ').split(' ', 2)
    print(search_images(url, depth))
