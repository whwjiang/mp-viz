import argparse
from time import sleep
from pymongo import errors
from .database import Database
from .scraper import UserScraper, RouteScraper

db = Database()
INTERVAL = .3

def user_scrape_and_insert(url):
    try:
        user = UserScraper(url)
    except:
        raise ValueError('invalid user')
    else:
        try:
            db.insert_doc(user.get_json(), 'user')
        except errors.DuplicateKeyError:
            db.update_doc(user.get_json(), 'user')
            print('{}: updated user'.format(user.id))
        else:
            print('{}: inserted user'.format(user.id))
        for url in user.get_route_urls():
            route_scrape_and_insert(url)
            sleep(INTERVAL)

def route_scrape_and_insert(url):
    try:
        route = RouteScraper(url)
    except:
        raise ValueError('invalid route')
    else:
        try:
            db.insert_doc(route.get_json(), 'route')
        except errors.DuplicateKeyError:
            db.update_doc(route.get_json(), 'route')
            print('{}: updated route'.format(route.id))
        else:
            print('{}: inserted route'.format(route.id))
