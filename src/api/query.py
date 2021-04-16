"""
query.py

Written by William Jiang on 04/09/2021

Parses a query for the API and returns a JSON corresponding to
the result of the query.

types of queries:

<user>+<user>%ticks: get common ticks between two users
<user>+<user>%todos: get common todos between two users
<user>+<user>%popular: get popular climb exclusive to either user
<user>+<user>%unpopular: get popular climb exclusive to either user
<user>%hardest-<type>: get hardest <type> climb in user's ticks
<user>+<user>%vis: get visualization formed from two users (not done)

"""

import sys
import pprint
import re
import argparse

from .compute import common, popular, unpopular, hardest
from .route import Route
from .retrieval.database import Database

QUERY_T = ('user', 
           'route', 
           'tick', 
           'todo', 
           'popular', 
           'unpopular', 
           'hardest',
           'vis',
           'all'
           )

ROUTE_T = ('boulder',
           'sport',
           'trad')

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
            self.__validate_inputs()
        except KeyError:
            # TODO: attempt a user scrape before doing this
            raise KeyError('input(s) are not in database')

    def send_request(self):
        if self.query_t == 'user':
            return self.__exec_user()
        if self.query_t == 'route':
            return self.__exec_route()
        self.__setup_compute()
        if self.query_t == 'todo' or self.query_t == 'tick':
            return self.__exec_common()
        if self.query_t == 'popular':
            return self.__exec_popular()
        if self.query_t == 'unpopular':
            return self.__exec_unpopular()
        if self.query_t == 'vis':
            return self.__exec_vis()
        if self.query_t == 'all':
            return self.__exec_all()
        return self.__exec_hardest()

    def __parse_query(self, q: str):
        pattern = '([0-9]+)\+?([0-9]+)?%([a-z]+)-?([a-z]+)?'
        m = re.search(pattern, q)

        if m is None or m.group(3) not in QUERY_T:
            raise Exception('invalid query')
        
        self.ids.append(m.group(1))
        if m.group(2):
            self.ids.append(m.group(2))
        self.query_t = m.group(3)
        if self.query_t == 'hardest' and m.group(4) not in ROUTE_T:
            raise Exception('invalid query')
        self.route_t = m.group(4)


    def __validate_inputs(self):
        if len(self.ids) == 2 and self.ids[0] == self.ids[1]:
            raise KeyError
        value = {'$in': self.ids}
        if self.query_t == 'route':
            if self.db.count_routes('_id', value) != len(self.ids):
                raise KeyError
        elif self.db.count_users('_id', value) != len(self.ids):
            raise KeyError
    
    def __setup_compute(self):
        users = self.db.find_users('_id', {'$in': self.ids})
        users_routes = []
        field = 'tick'
        if self.query_t == 'todo':
            field = 'todo'
        for doc in users:
            users_routes.append(doc[field])
        
        self.routes = []

        for route_list in users_routes:
            q = self.db.find_routes('_id', {'$in': route_list})
            self.routes.append([Route(item) for item in q])
    
    def __exec_user(self):
        result = self.db.find_user('_id', {'$in': self.ids})
        return {'user': result}

    def __exec_route(self):
        result = self.db.find_route('_id', {'$in': self.ids})
        return {'route': result}

    def __exec_common(self):
        common_list = common(self.routes[0], self.routes[1])
        return {self.query_t: [vars(item) for item in common_list]}

    def __exec_popular(self):
        route_list = popular(self.routes[0], self.routes[1])
        return {self.query_t: [vars(item) if item else None for item in route_list]}

    def __exec_unpopular(self):
        route_list = unpopular(self.routes[0], self.routes[1])
        return {self.query_t: [vars(item) if item else None for item in route_list]}

    def __exec_hardest(self):
        route_list = [i for i in self.routes[0] if i.type.lower() == self.route_t]
        return {self.query_t: vars(hardest(route_list))}

    def __exec_vis(self):
        pass

    def __exec_all(self):
        
     