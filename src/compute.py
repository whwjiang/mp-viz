"""

compute.py

Written by William Jiang 04/07/2021

Computes different things on lists of climbs.
Things computable:
- number of ticks in common
- number of to-dos in common
- most popular climb in tick list exclusive to either list
- hardest climb exclusive to either tick list

"""

from route import Route
"""
class Compute:
    def __init__(self, l0: list, l1: list):
        self.lists = []
        self.lists.append([Route(item) for item in l0])
        self.lists.append([Route(item) for item in l1])

        self.sets = []
        self.sets.append(set(lists[0]))
        self.sets.append(set(lists[1]))
"""


def common(l1: list, l2: list) -> list:
    """


    """
    if l1 is None or l2 is None:
        return []

    s1 = set(l1)
    s2 = set(l2)
    s3 = s1.intersection(s2)
    return list(s3)

def popular(l1: list, l2: list) -> (Route, Route):
    """

    """

    if l1 is None or l2 is None:
        return (None, None)

    s1 = set(l1)
    s2 = set(l2)
    s1_exclusive = s1.difference(s2)
    s2_exclusive = s2.difference(s1)

    p1 = None
    if s1_exclusive:
        p1 = max(s1_exclusive, key = lambda k: k.rating_count)
    p2 = None
    if s2_exclusive:
        p2 = max(s2_exclusive, key = lambda k: k.rating_count)

    return (p1, p2)

def unpopular(l1: list, l2: list) -> (Route, Route):
    """

    """

    if l1 is None or l2 is None:
        return (None, None)

    s1 = set(l1)
    s2 = set(l2)
    s1_exclusive = s1.difference(s2)
    s2_exclusive = s2.difference(s1)

    p1 = None
    if s1_exclusive:
        p1 = min(s1_exclusive, key = lambda k: k.rating_count)
    p2 = None
    if s2_exclusive:
        p2 = min(s2_exclusive, key = lambda k: k.rating_count)

    return (p1, p2)

def hardest(l: list) -> Route:
    """

    """

    hard = max(l, key = lambda k: k.grade_to_int())
    return hard
