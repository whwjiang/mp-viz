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
            print('{}: user already inserted'.format(user.id))
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
            print('{}: route already inserted'.format(route.id))
        else:
            print('{}: inserted route'.format(route.id))

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
