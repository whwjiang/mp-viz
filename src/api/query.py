"""
query.py

Written by William Jiang on 04/09/2021

Parses a query for the API and result =s a JSON corresponding to
the result of the query.

types of queries:

<user>%user: get user information for <user>
<route>%route: get route information for <route>
<user>+<user>%ticks: get common ticks between two users
<user>+<user>%todos: get common todos between two users
<user>+<user>%popular: get popular climb exclusive to either user
<user>+<user>%unpopular: get popular climb exclusive to either user
<user>%hardest-<type>: get hardest <type> climb in user's ticks
<user>+<user>%vis: get visualization formed from two users (not done)

<user>+<user>%all: get all components

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
        result = None
        if self.query_t == 'user':
            result = self.__exec_user()
        elif self.query_t == 'route':
            result = self.__exec_route()
        else:
            self.__setup_compute()
            if self.query_t == 'all':
                result = self.__exec_all()
            elif self.query_t == 'todo' or self.query_t == 'tick':
                result = self.__exec_common()
            elif self.query_t == 'popular':
                result = self.__exec_popular()
            elif self.query_t == 'unpopular':
                result = self.__exec_unpopular()
            elif self.query_t == 'vis':
                result = self.__exec_vis()
            else:
                result = self.__exec_hardest()
        return {self.query_t: result}

    def __parse_query(self, q: str):
        pattern = '([0-9]+)\+?([0-9]+)?%(.+)'
        m = re.search(pattern, q)

        if m is None or m.group(3) not in QUERY_T:
            raise Exception('invalid query')
        
        self.ids.append(m.group(1))
        if m.group(2):
            self.ids.append(m.group(2))
        self.query_t = m.group(3)

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
        self.users = [i for i in self.db.find_users('_id', {'$in': self.ids})]
        users_todos = []
        users_ticks = []
        for doc in self.users:
            users_todos.append(doc['todo'])
            users_ticks.append(doc['tick'])
        
        # these are lists of lists s.t. list[0] corresponds to user0
        self.todos = []
        self.ticks = []

        for todo_list in users_todos:
            q = self.db.find_routes('_id', {'$in': todo_list})
            self.todos.append([Route(item) for item in q])
        
        for tick_list in users_ticks:
            q = self.db.find_routes('_id', {'$in': tick_list})
            self.ticks.append([Route(item) for item in q])
    
    def __exec_user(self):
        return self.db.find_user('_id', {'$in': self.ids})

    def __exec_route(self):
        return self.db.find_route('_id', {'$in': self.ids})

    def __exec_common(self):
        common_list = []
        if self.query_t == 'tick':
            common_list = common(self.ticks[0], self.ticks[1])
        if self.query_t == 'todo':
            common_list = common(self.todos[0], self.todos[1])
        return [vars(item) for item in common_list]

    def __exec_popular(self):
        pair = popular(self.ticks[0], self.ticks[1])
        return [vars(i) if i else None for i in pair]

    def __exec_unpopular(self):
        pair = unpopular(self.ticks[0], self.ticks[1])
        return [vars(i) if i else None for i in pair]

    def __exec_hardest(self):
        hard_dict = {}
        boulder = hardest(filter(lambda x: x.type == 'Boulder', self.ticks[0]))
        hard_dict['boulder'] = vars(boulder) if boulder else None
        sport = hardest(filter(lambda x: x.type == 'Sport', self.ticks[0]))
        hard_dict['sport'] = vars(sport) if sport else None
        trad = hardest(filter(lambda x: x.type == 'Trad', self.ticks[0]))
        hard_dict['trad'] = vars(trad) if trad else None
        return hard_dict

    def __exec_vis(self):
        # TODO: implement vis
        return {}

    def __exec_all(self):
        result = {}
        result['users'] = self.users
        self.query_t = 'tick'
        result['tick'] = self.__exec_common()
        self.query_t = 'todo'
        result['todo'] = self.__exec_common()
        result['popular'] = self.__exec_popular()
        result['unpopular'] = self.__exec_unpopular()
        result['hardest'] = [self.__exec_hardest()]
        self.ticks[0], self.ticks[1] = self.ticks[1], self.ticks[0]
        result['hardest'].append(self.__exec_hardest())
        self.query_t = 'all'

        return result

     