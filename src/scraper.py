"""
scraper.py

Written by William Jiang 04/02/2021

Contains classes for scraping user and route info from
mountainproject.com

"""

import logging
from bs4 import BeautifulSoup
import requests

DOMAIN = 'www.mountainproject.com'

class UserScraper:
    """
    takes a url pointing to a mountainproject user and scrapes
    useful information from the user's profile
    """
    def __init__(self, url):
        self.url = url

        address = url.split('/')
        if address[2] != DOMAIN:
            raise Exception('not a mountain project page')
        if address[3] != 'user':
            raise Exception('not a user')

        page = requests.get(url)
        if page.status_code != 200:
            raise Exception('invalid url')

        self.soup = BeautifulSoup(page.content, 'html.parser')

        self.dict          = {}
        self.route_urls    = []
        self.id            = address[4]
        self.dict['_id']   = self.id
        self.dict['url']   = url

        self.__parse_elements()

    def get_json(self):
        """
        returns a dict filled out with information from user's
        MP profile.
        """
        return self.dict

    def get_route_urls(self):
        """
        returns a list of urls pointing to routes in user's todos
        and ticks.
        """
        return self.route_urls

    def __parse_elements(self):
        try:
            self.__parse_name()
        except:
            logging.info('{}: missing name'.format(self.id))

        self.__parse_avatar_url()
        self.__parse_routes('todos')
        self.__parse_routes('ticks')


    def __parse_name(self):
        name = self.soup.find(class_='dont-shrink mb-0')

        try:
            self.dict['name'] = name.get_text().strip()
        except:
            self.dict['name'] = ''
            raise

    def __parse_avatar_url(self):
        url = self.soup.find(class_='user-img-avatar lazy').get('data-original')
        if url == '/img/user/missing2.svg':
            url = 'https://www.mountainproject.com/img/user/missing2.svg'
        self.dict['avatar_url'] = url

    def __parse_routes(self, kind):
        url = '{}/ticks'.format(self.url)
        if kind == 'todos':
            url = '{}/climb-todo-list'.format(self.url)
        page = requests.get(url)

        if page.status_code != 200:
            raise Exception('invalid url')

        todo_soup = BeautifulSoup(page.content, 'html.parser')
        rows = todo_soup.find_all(class_='route-row')
        routes = {}
        for i in rows:
            try:
                route_url = i.find('a').get('href')
            except:
                pass
            else:
                self.route_urls.append(route_url)
                routes[route_url.split('/')[4]] = 1

        self.dict[kind] = list(routes.keys())

class RouteScraper:
    """
    Takes a url pointing to a route on MP and scrapes important
    information
    """
    def __init__(self, url):
        self.url = url
        address = url.split('/')
        if address[2] != DOMAIN:
            raise Exception('not a mountain project page')
        if address[3] != 'user':
            raise Exception('not a user')

        page = requests.get(url)
        if page.status_code != 200:
            raise Exception('invalid url')

        self.soup = BeautifulSoup(page.content, 'html.parser')

        self.dict          = {}
        self.id            = address[4]
        self.dict['_id']   = self.id
        self.dict['url']   = url
        self.dict['image_urls'] = []

        self.__parse_elements()

    def get_json(self):
        """
        Returns a dict filled with information from scraping
        """
        return self.dict

    def __parse_elements(self):
        self.__parse_info()
        self.__parse_type()
        self.__parse_pics()

    def __parse_info(self):
        info = self.soup.find(class_='col-md-9 float-md-right mb-1')
        self.dict['name'] = info.find('h1').get_text().strip()
        self.dict['grade'] = info.find(class_='rateYDS').get_text().split()[0]
        score = info.find('span', {'id': 'route-star-avg'}).get_text().split()
        self.dict['rating'] = score[1]
        self.dict['rating_count'] = score[3]

    def __parse_type(self):
        table = self.soup.find('table', {'class': 'description-details'})
        row = table.find('tr')
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        self.dict['type'] = cols[1].split(',')[0]

    def __parse_pics(self):
        url = '{}?print=1'.format(self.url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        imgs = soup.find_all(class_='lazy img-fluid')
        self.dict['image_urls'] = [img.get('data-src') for img in imgs if img.get('data-src')]
