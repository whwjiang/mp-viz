import filecmp
import json
import os
import unittest
import pymongo
import sys

sys.path.append('/home/whjiang/coding/cs242/sp21-cs242-project/src')

from database import Database
db = Database()

class database_tests(unittest.TestCase):

    def test_insert_user(self):
        import_file = open('user.json', 'r')
        data = json.load(import_file)
        result = db.insert_doc(data, 'user')
        self.assertIsNotNone(result)
        db.db['user'].delete_one({'_id': '0'})
        import_file.close()

    def test_insert_route(self):
        import_file = open('route.json', 'r')
        data = json.load(import_file)
        result = db.insert_doc(data, 'route')
        self.assertIsNotNone(result)
        db.db['route'].delete_one({'_id': '0'})
        import_file.close()

    def test_bad_route(self):

if __name__ == '__main__':
    unittest.main()
