import filecmp
import json
import os
import unittest
import pymongo
import sys

sys.path.append('..')

from src.api.retrieval.scraper import UserScraper, RouteScraper

class scraper_tests(unittest.TestCase):
    def test_bad_user_domain(self):
        with self.assertRaises(Exception) as context:
            user = UserScraper('https://google.com')

    def test_bad_route_domain(self):
        with self.assertRaises(Exception) as context:
            route = RouteScraper('https://google.com')

    def test_UserScraper_non_user(self):
        with self.assertRaises(Exception) as context:
            user = UserScraper('https://www.mountainproject.com/route/107813267/unfinished-symphony')

    def test_RouteScraper_non_route(self):
        with self.assertRaises(Exception) as context:
            route = RouteScraper('https://www.mountainproject.com/user/107457346/nathan-mowery')

    def test_bad_user_url(self):
        with self.assertRaises(Exception) as context:
            user = UserScraper('https://www.wdaidhwhudwika.com/route/107813267/unfinished-symphony')

    def test_bad_route_url(self):
        with self.assertRaises(Exception) as context:
            route = RouteScraper('https://www.wdaidhwhudwika.com/route/107813267/unfinished-symphony')

if __name__ == '__main__':
    unittest.main()
