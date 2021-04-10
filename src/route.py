"""

route.py

Written by William Jiang on 04/07/2020

A container class for route information

"""
import re

from dataclasses import dataclass

@dataclass(unsafe_hash=True)
class Route:
    """
    member variables are lifted from database entries
    database entry must have all entries, so no point in checking for
    key errors in json

    """
    def __init__(self, json):
        self._id = json['_id']
        self.url = json['url']
        self.image_urls = json['image_urls']
        self.name = json['name']
        self.grade = json['grade']
        self.rating_count = json['rating_count']
        self.type = json['type']

    def grade_to_int(self):
        """
        converts the route grade to an arbitrary int to then be compared
        to other grades based on type

        @returns:
        score representing machine interpretable difficulty of a climb
        """
        if self.type == 'Boulder':
            score = 5
            pattern = 'V([1]?[0-9])(-[1]?[0-9])?([+,-])?'
            match = re.search(pattern, self.grade)
            score += int(match.group(1)) * 10
            if match.group(2):
                score += 4
            elif match.group(3) == '-':
                score -= 2
            elif match.group(3) == '+':
                score += 2
            return score

        """
        total ordering of minor grade modifiers:
        a, -, a/b, b, none, b/c, c, +, c/d, d
        """
        score = 4
        pattern = '5(\.[1]?[0-9])([+,-])?(a/b|b/c|c/d)?([a-d])?'
        match = re.search(pattern, self.grade)
        # TODO: implement parsing for ice climbing, other systems
        if match is None:
            return score
        score += int(match.group(1)) * 10
        if match.group(2) == '+':
            score += 3
        elif match.group(2) == '-':
            score -= 3
        elif match.group(3) == 'a/b':
            score -= 2
        elif match.group(3) == 'b/c':
            score += 1
        elif match.group(3) == 'c/d':
            score += 4
        elif match.group(4) == 'a':
            score -= 4
        elif match.group(4) == 'b':
            score -= 1
        elif match.group(4) == 'c':
            score -= 2
        elif match.group(4) == 'd':
            score += 5
        return score

    def __eq__(self, other):
        return self._id == other._id
    
    def __str__(self):
        return 'Name: {}'.format(self.name)
