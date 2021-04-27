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
import math
from .route import Route

def common(l1: list, l2: list) -> list:
    """
    computes all routes in common between two lists
    @params:
    l1: list of routes
    l2: list of routes

    @returns:
    set intersection of l1 and l2
    """
    if l1 is None or l2 is None:
        return []

    s1 = set(l1)
    s2 = set(l2)
    s3 = s1.intersection(s2)
    return list(s3)

def popular(l1: list, l2: list) -> (Route, Route):
    """
    computes two routes that have the highest rating exclusive 
    to either list

    @params:
    l1: list of routes
    l2: list of routes

    @returns:
    p1: highest rated route exclusive to the first list
    p2: highest rated route exclusive to the second list
    """

    if l1 is None or l2 is None:
        return (None, None)

    s1 = set(l1)
    s2 = set(l2)
    s1_exclusive = s1.difference(s2)
    s2_exclusive = s2.difference(s1)

    p1 = None
    if s1_exclusive:
        p1 = max(s1_exclusive, key = lambda k: int(k.rating_count))
    p2 = None
    if s2_exclusive:
        p2 = max(s2_exclusive, key = lambda k: int(k.rating_count))

    return (p1, p2)

def unpopular(l1: list, l2: list) -> (Route, Route):
    """
    computes two routes that have the lowest rating count 
    exclusive to either list
    
    @params:
    l1: list of routes
    l2: list of routes

    @returns:
    p1: least rated route exclusive to the first list
    p2: least rated route exclusive to the second list
    """

    if l1 is None or l2 is None:
        return (None, None)

    s1 = set(l1)
    s2 = set(l2)
    s1_exclusive = s1.difference(s2)
    s2_exclusive = s2.difference(s1)

    p1 = None
    if s1_exclusive:
        p1 = min(s1_exclusive, key = lambda k: float(k.rating))
    p2 = None
    if s2_exclusive:
        p2 = min(s2_exclusive, key = lambda k: float(k.rating))

    return (p1, p2)

def hardest(l: list) -> Route:
    """
    returns the hardest climb in l. assumes l has all the same type of
    route.

    @params:
    l: list of routes

    @returns:
    hard: the hardest route in l
    """

    try:
        hard = max(l, key = lambda k: k.grade_to_int())
    except ValueError:
        return None
    else:
        return hard

def _compute_node_size(rating_count: str):
    return int(math.log(int(rating_count))) + 1

def _route_to_edge(route: Route, user: str) -> dict:
    edge = {
        'id': 'e{}-{}'.format(route._id, user), 
        'source': user, 
        'target': route._id
    }
    return edge

def _route_to_node(route: Route) -> dict:
    node = {
        'id': route._id, 
        'label': route.name, 
        'color': '#fcba03', 
        'size': _compute_node_size(route.rating_count),
        'x': 0,
        'y': 0
    }
    return node


def vis(users: list, l1: list, l2: list) -> dict:
    """
    creates a network based on the two lists and the users

    @params
    users: a list of users (max: 2)
    l1: list of routes that corresponds to users[0]
    l2: list of routes that corresponds to users[1]

    @returns:
    dict that is a graph parsable by sigma.js
    """
    edges = []
    nodes = []

    nodes.append({
        'id': users[0]['_id'],
        'label': users[0]['name'],
        'color': '#43d5fa',
        'size': 11,
        'x': -10,
        'y': 0
    })

    nodes.append({
        'id': users[1]['_id'],
        'label': users[1]['name'],
        'color': '#32a852',
        'size': 11,
        'x': 10,
        'y': 0
    })

    s1 = set(l1)
    s2 = set(l2)
    s3 = s1.union(s2)

    edges += list(map(lambda x: _route_to_edge(x, users[0]['_id']), s1))
    edges += list(map(lambda x: _route_to_edge(x, users[1]['_id']), s2))

    nodes += list(map(_route_to_node, s3))

    return {'nodes': nodes, 'edges': edges}
