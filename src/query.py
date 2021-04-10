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

import pprint
import re
import argparse

import compute
from route import Route
from database import Database

QUERY_T = ('ticks', 'todos', 'popular', 'unpopular', 'hardest', 'vis')

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

    def send_request(self):
        if self.query_t == 'todos' or self.query_t == 'ticks':
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
        result = self.db.query_users('_id', {'$in': self.ids})
        routes = []
        for doc in result:
            routes.append(doc.get(self.query_t))

        q0 = self.db.query_routes('_id', {'$in': routes[0]})
        l0 = [Route(item) for item in q0]
        q1 = self.db.query_routes('_id', {'$in': routes[1]})
        l1 = [Route(item) for item in q1]

        for item in l0:
            print(item)
        print(len(l0))

        

    def __exec_popular(self):
        pass

    def __exec_unpopular(self):
        pass

    def __exec_hardest(self):
        pass

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
