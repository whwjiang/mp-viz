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
        self.assertEqual(result.inserted_id, '0')
        db.db['user'].delete_one({'_id': '0'})
        import_file.close()

    def test_insert_route(self):
        import_file = open('route.json', 'r')
        data = json.load(import_file)
        result = db.insert_doc(data, 'route')
        self.assertEqual(result.inserted_id, '0')
        db.db['route'].delete_one({'_id': '0'})
        import_file.close()

    def test_bad_user_insertion(self):
        import_file = open('user.json', 'r')
        data = json.load(import_file)
        import_file.close()
        with self.assertRaises(AttributeError) as context:
            db.insert_doc(data, 'use')

    def test_bad_route_insertion(self):
        import_file = open('route.json', 'r')
        data = json.load(import_file)
        import_file.close()
        with self.assertRaises(AttributeError) as context:
            db.insert_doc(data, 'rout')

    def test_bad_user_update(self):
        import_file = open('user.json', 'r')
        data = json.load(import_file)
        import_file.close()
        with self.assertRaises(AttributeError) as context:
            db.update_doc(data, 'use')

    def test_bad_route_update(self):
        import_file = open('route.json', 'r')
        data = json.load(import_file)
        import_file.close()
        with self.assertRaises(AttributeError) as context:
            db.update_doc(data, 'rout')

    def test_query_user(self):
        import_file = open('user.json', 'r')
        data = json.load(import_file)
        db.insert_doc(data, 'user')
        result = db.query_users('_id', '0')
        self.assertEqual(len(list(result)), 1)
        db.db['user'].delete_one({'_id': '0'})
        import_file.close()

    def test_query_route(self):
        import_file = open('route.json', 'r')
        data = json.load(import_file)
        db.insert_doc(data, 'route')
        result = db.query_routes('_id', '0')
        self.assertEqual(len(list(result)), 1)
        db.db['route'].delete_one({'_id': '0'})
        import_file.close()

    def test_non_user_query(self):
        result = db.query_users('_id', '-1')
        self.assertEqual(len(list(result)), 0)

    def test_non_route_query(self):
        result = db.query_routes('_id', '-1')
        self.assertEqual(len(list(result)), 0)

    def test_update_nonexistent_user(self):
        import_file = open('user.json', 'r')
        data = json.load(import_file)
        import_file.close()
        result = db.update_doc(data, 'user')
        self.assertEqual(result.matched_count, 0)

    def test_update_nonexistent_route(self):
        import_file = open('route.json', 'r')
        data = json.load(import_file)
        import_file.close()
        result = db.update_doc(data, 'route')
        self.assertEqual(result.matched_count, 0)

    def test_update_user(self):
        import_file = open('user.json', 'r')
        data = json.load(import_file)
        import_file.close()
        db.insert_doc(data, 'user')
        data['url'] = 'google.com'
        result = db.update_doc(data, 'user')
        self.assertEqual(result.matched_count, 1)
        db.db['user'].delete_one({'_id': '0'})

    def test_update_route(self):
        import_file = open('route.json', 'r')
        data = json.load(import_file)
        import_file.close()
        db.insert_doc(data, 'route')
        data['url'] = 'google.com'
        result = db.update_doc(data, 'route')
        self.assertEqual(result.matched_count, 1)
        db.db['route'].delete_one({'_id': '0'})


if __name__ == '__main__':
    unittest.main()
