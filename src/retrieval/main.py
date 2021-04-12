import argparse
import time
from pymongo import errors
from scraper import UserScraper, RouteScraper
from database import Database

db = Database()

def route_scrape_and_insert(url):
    route = RouteScraper(url)
    try:
        db.insert_doc(route.get_json(), 'route')
    except errors.DuplicateKeyError:
        print('{}: route already inserted'.format(route.id))
    else:
        print('{}: inserted route'.format(route.id))

def user_scrape_and_insert(url):
    user = UserScraper(url)
    try:
        db.insert_doc(user.get_json(), 'user')
    except errors.DuplicateKeyError:
        print('{}: user already inserted'.format(user.id))
    else:
        print('{}: inserted user'.format(user.id))
    for url in user.get_route_urls():
        route_scrape_and_insert(url)
        time.sleep(.3)

def main():
    parser = argparse.ArgumentParser(description='Mountain Project scraper')
    kind = parser.add_mutually_exclusive_group()
    kind.add_argument('-u', '--user', nargs=1, help='scrape a user')
    kind.add_argument('-r', '--route', nargs=1, help='scrape a route')

    args = parser.parse_args()

    if args.user:
        user_scrape_and_insert(args.user[0])

    if args.route:
        route_scrape_and_insert(args.route[0])


if __name__ == "__main__":
    main()
