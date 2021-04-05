"""
database.py

Written by William Jiang on 04/02/2021

Contains wrappers for interfacing with a MongoDB database

"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv

URL = 'mongodb+srv://{}:{}@cluster0.f0mds.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

class Database:
    """
    Utilizes pymongo to interface with a MongoDB database. Has methods for
    insertion, updating, and finding
    """
    def __init__(self):
        load_dotenv()
        user = os.environ.get('USER')
        token = os.environ.get('TOKEN')
        self.client = MongoClient(URL.format(user, token))

        self.db = self.client['mp']

    def insert_doc(self, json, col):
        """
        inserts a json doc in the collection specified by col

        @params:
        json: dictionary to be inserted
        col: the collection being inserted to (user or route)

        @returns:
        result: the result of insertion into the database
        """
        if col not in ('user', 'route'):
            raise AttributeError
        result = self.db[col].insert_one(json)
        return result

    def update_doc(self, json, col):
        """
        updates a MongoDB doc identified by json['_id'] with the contents
        of json in the collection specified by col

        @params:
        json: the information that will be used to update stuff
        col: the collection being inserted to (user or route)

        @returns:
        result: the result of update in the database
        """
        if col not in ('user', 'route'):
            raise AttributeError
        result = self.db[col].update_one({'_id': json['_id']}, {'$set': json})
        return result

    def query_users(self, field, value):
        """
        finds all MongoDB users pertaining to the value at field

        @params:
        field: the property being found
        value: the value of the field being queried

        @returns:
        users: the result of query in the database
        """
        try:
            users = self.db['user'].find({field: value})
        except:
            raise Exception
        else:
            return users

    def query_routes(self, field, value):
        """
        finds all MongoDB routes pertaining to the value at field

        @params:
        field: the property being found
        value: the value of the field being queried

        @returns:
        routes: the result of query in the database
        """
        try:
            routes = self.db['route'].find({field: value})
        except:
            raise Exception
        else:
            return routes
