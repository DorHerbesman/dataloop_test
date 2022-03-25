import requests as rq
import os
from bs4 import *
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import validators
import time


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


def search_images(url, max_level):
    primary_links = get_links(url, 0)


    for level, link in list(primary_links.values()):
        valid = validators.url(link)
        if valid:
             if level <= max_level:
                level += 1
                links = get_links(link, level)
                for new_link in links:
                    if new_link not in primary_links:
                        primary_links[new_link] = [level, new_link]

    dict_to_return = {}

    for level, link in primary_links.values():
        valid = validators.url(link)
        if valid:
            r = rq.get(link)
            soup = BeautifulSoup(r.text, "html.parser")
            images = soup.findAll('img')
            for image in images:
                dict_to_return['results'] = {'imageUrl: ': image, 'sourceUrl: ': link, 'depth: ': level}

    return dict_to_return

if __name__ == '__main__':
    val = input('please enter url and depth seperated by space ').split(' ',2)
    print(search_images('https://www.geeksforgeeks.org/',3))
