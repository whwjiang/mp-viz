import filecmp
import json
import os
import unittest
import pymongo
import sys
from pprint import pprint

sys.path.append('..')

from src.api.query import Query
from src.api.retrieval.database import Database
db = Database()

class query_tests(unittest.TestCase):

    def test_hardest(self):
        q = Query('0%hardest')
        result = q.send_request()
        route_file = open('json/route0.json', 'r')
        route_data = json.load(route_file)
        self.assertEqual(result['hardest']['boulder'], route_data)
        route_file.close()

    def test_popular(self):
        q = Query('0+1%popular')
        result = q.send_request()
        route0_file = open('json/route0.json', 'r')
        route0_data = json.load(route0_file)
        route0_file.close()
        route1_file = open('json/route1.json', 'r')
        route1_data = json.load(route1_file)
        route1_file.close()
        self.assertEqual(result['popular'][0], route0_data)
        self.assertEqual(result['popular'][1], route1_data)

    def test_unpopular(self):
        q = Query('0+1%unpopular')
        result = q.send_request()
        route0_file = open('json/route0.json', 'r')
        route0_data = json.load(route0_file)
        route0_file.close()
        route1_file = open('json/route1.json', 'r')
        route1_data = json.load(route1_file)
        route1_file.close()
        self.assertEqual(result['unpopular'][0], route0_data)
        self.assertEqual(result['unpopular'][1], route1_data)
    
    def test_todo_success(self):
        q = Query('0+1%todo')
        result = q.send_request()
        self.assertEqual(len(result['todo']), 1)

    def test_tick_failure(self):
        q = Query('0+1%tick')
        result = q.send_request()
        self.assertEqual(len(result['tick']), 0)

    def test_invalid_query(self):
        with self.assertRaises(Exception) as context:
            q = Query('0+1%tock')
    
    def test_bad_users(self):
        with self.assertRaises(KeyError) as context:
            q = Query('2+3%tick')

    def test_duplicate_users_error(self):
        with self.assertRaises(KeyError) as context:
            q = Query('2+2%tick')

    def test_query_user(self):
        q = Query('0%user')
        result = q.send_request()
        user0_file = open('json/user0.json', 'r')
        user0_data = json.load(user0_file)
        user0_file.close()
        self.assertEqual(result['user'], user0_data)
    
    def test_query_route(self):
        q = Query('0%route')
        result = q.send_request()
        route0_file = open('json/route0.json', 'r')
        route0_data = json.load(route0_file)
        route0_file.close()
        self.assertEqual(result['route'], route0_data)

    def test_malformed_single_query(self):
        with self.assertRaises(Exception) as context:
            q = Query('0%boi')

    def test_bad_single_query_user(self):
        with self.assertRaises(KeyError) as context:
            q = Query('3%user')

    def test_hardest_invalid_route_t(self):
        with self.assertRaises(Exception) as context:
            q = Query('0%hardest-blob')

    def test_request_vis_empty(self):
        q = Query('0+1%vis')
        self.assertTrue(True)

    def test_all(self):
        q = Query('200305518+200696013%all')
        result = q.send_request()
        pprint(result)


if __name__ == '__main__':
    unittest.main()
