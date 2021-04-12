"""
query.py

Written by William Jiang on 04/09/2021

Parses a query for the API and returns a JSON corresponding to
the result of the query.

types of queries:

<user>&<user>?ticks: get common ticks between two users
<user>&<user>?todos: get common todos between two users
<user>&<user>?popular: get popular climb exclusive to either user
<user>&<user>?unpopular: get popular climb exclusive to either user
<user>?hardest: get hardest boulder and rope climb in user's ticks
<user>&<user>?vis: get visualization formed from two users (not done)

"""

sys.path.append('../retrieval')

import pprint
import re
import argparse

import compute
from route import Route
from database import Database

QUERY_T = ('tick', 'todo', 'popular', 'unpopular', 'hardest', 'vis')

class Query:
    """
    contains logic for parsing and executing a query from the database
    """

    def __init__(self, q: str):
        self.ids = []
        try:
            self.__parse_query(q)
        except:
            raise Exception('invalid query')

        self.db = Database()
        try:
            self.__validate_users()
        except KeyError:
            # TODO: attempt a user scrape before doing this
            raise KeyError('user(s) are not in database')

        users = self.db.query_users('_id', {'$in': self.ids})
        users_routes = []
        for doc in users:
            users_routes.append(doc[self.query_t])
        
        self.routes = []

        for route_list in users_routes:
            q = self.db.query_routes('_id', {'$in': route_list})
            self.routes.append([Route(item) for item in q])

    def send_request(self):
        if self.query_t == 'todo' or self.query_t == 'tick':
            self.__exec_common()
            return
        if self.query_t == 'popular':
            self.__exec_popular()
            return
        if self.query_t == 'unpopular':
            self.__exec_unpopular()
            return
        if self.query_t == 'hardest':
            self.__exec_hardest()
            return
        if self.query_t == 'vis':
            self.__exec_vis()
            return
        return

    def __parse_query(self, q: str):
        pattern = '([0-9]+)&?([0-9]+)?\?([a-z]+)'
        m = re.search(pattern, q)

        if m is None or m.group(3) not in QUERY_T:
            raise Exception('invalid query')
        
        self.ids.append(m.group(1))
        self.ids.append(m.group(2))
        self.query_t = m.group(3)

    def __validate_users(self):
        value = {'$in': self.ids}
        if self.db.count_users('_id', value) != len(self.ids):
            raise KeyError
    
    def __exec_common(self):
        common_list = compute.common(self.routes[0], self.routes[1])
        return {self.query_t: [vars(item) for item in common_list]}

    def __exec_popular(self):
        popular = compute.popular(self.routes[0], self.routes[1])
        return {self.query_t: [vars(item) for item in popular]}

    def __exec_unpopular(self):
        unpopular = compute.unpopular(self.routes[0], self.routes[1])
        return {self.query_t: [vars(item) for item in unpopular]}

    def __exec_hardest(self):
        return {self.query_t: compute.hardest(self.routes[0])}

    def __exec_vis(self):
        pass
     

def main():
    parser = argparse.ArgumentParser(description='query static info')
    parser.add_argument('-q', '--query', nargs=1, help='query info')

    args = parser.parse_args()

    q = Query(args.query[0])
    q.send_request()

if __name__ == '__main__':
    main()
