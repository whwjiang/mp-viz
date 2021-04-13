import filecmp
import json
import os
import unittest
import pymongo
import sys

sys.path.append('..')

BASIC_ROUTE = {"_id":"0","url":"","image_urls":[],"name":"","grade":"V0","rating":"0.0","rating_count":"0","type":"Boulder"}

from src.api import compute
from src.api.route import Route 

class compute_tests(unittest.TestCase):
    def test_common_success(self):
        l1 = [Route(BASIC_ROUTE)]
        l2 = [Route(BASIC_ROUTE)]
        l3 = compute.common(l1, l2)
        self.assertEqual(len(l3), 1)

    def test_common_failure(self):
        modified_route = BASIC_ROUTE.copy()
        modified_route['_id'] = '1'
        l1 = [Route(modified_route)]
        l2 = [Route(BASIC_ROUTE)]
        l3 = compute.common(l1, l2)
        self.assertEqual(len(l3), 0)

    def test_popular_success(self):
        r1 = BASIC_ROUTE.copy()
        r2 = BASIC_ROUTE.copy()
        r1['_id'] = '10'
        l1 = [Route(r1)]
        l2 = [Route(r2)]
        p1, p2 = compute.popular(l1, l2)
        self.assertEqual(Route(r1), p1)
        self.assertEqual(Route(r2), p2)

    def test_popular_failure(self):
        r1 = BASIC_ROUTE.copy()
        r2 = BASIC_ROUTE.copy()
        l1 = [Route(r1)]
        l2 = [Route(r2)]
        p1, p2 = compute.popular(l1, l2)
        self.assertIsNone(p1)
        self.assertIsNone(p2)

    def test_hardest(self):
        l = [Route(BASIC_ROUTE) for i in range(0, 10)]
        r_hard = BASIC_ROUTE.copy()
        r_hard['grade'] = 'V17'
        r_hard['_id'] = '2'
        r_hard = Route(r_hard)
        l.append(r_hard)
        hardest = compute.hardest(l)
        self.assertEqual(r_hard, hardest)
    
    def test_hardest_failure(self):
        l = []
        hardest = compute.hardest(l)
        self.assertIsNone(hardest)

if __name__ == '__main__':
    unittest.main()
