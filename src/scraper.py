from bs4 import BeautifulSoup
from enum import Enum
import requests

class UserFields(Enum):
    _id        = 1
    name       = 2
    ticks      = 3
    todos      = 4
    avatar_url = 5

class RouteFields(Enum):
    _id      = 1
    name     = 2
    type     = 3
    grade    = 4
    rating   = 5
    fa       = 6
    pic_urls = 7

class UserScraper:
    def __init__(self, url):
        self.url = url
        page = requests.get(url)

        if page.status_code != 200:
            raise Exception('invalid url')

        address = url.split('/')
        if address[3] != 'user':
            raise Exception('not a user')

        self.soup = BeautifulSoup(page.content, 'html.parser')

        self.dict          = {}
        self.route_urls    = []
        self.id            = address[4]
        self.dict['_id']   = self.id
        self.dict['url']   = url

        self.__parse_elements()

    def get_dict(self):
        return self.dict

    def get_route_urls(self):
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
            raise

    def __parse_avatar_url(self):
        url = self.soup.find(class_='user-img-avatar lazy').get('data-original')
        if url == '/img/user/missing2.svg':
            url = 'https://www.mountainproject.com/img/user/missing2.svg'
        self.dict['avatar_url'] = url

    def __parse_routes(self, type):
        url = '{}/ticks'.format(self.url)
        if type == 'todos':
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

        self.dict[type] = list(routes.keys())

class RouteScraper:
    def __init__(self, url):
