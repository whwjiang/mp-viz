import argparse

from pymongo import errors
from scraper import UserScraper, RouteScraper
from database import Database

def main():
    parser = argparse.ArgumentParser(description='Mountain Project scraper')
    kind = parser.add_mutually_exclusive_group()
    kind.add_argument('-u', '--user', nargs=1, help='scrape a user')
    kind.add_argument('-r', '--route', nargs=1, help='scrape a route')

    args = parser.parse_args()
    db = Database()

    if args.user:
        user = UserScraper(args.user[0])
        try:
            result = db.insert_doc(user.get_json(), 'user')
        except errors.DuplicateKeyError:
            print('error, already inserted')
        else:
            print('inserted user {}'.format(result))

    if args.route:
        route = RouteScraper(args.route[0])
        try:
            result = db.insert_doc(route.get_json(), 'route')
        except errors.DuplicateKeyError:
            print('error, already inserted')
        else:
            print('inserted route {}'.format(result))


if __name__ == "__main__":
    main()
