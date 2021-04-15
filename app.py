#!/usr/bin/env python3
"""

app.py

Written by William Jiang 04/07/2021

Contains APIs for mpviz: data, graph, computation

"""

import json
import sys
import os

from flask import Flask, jsonify, request, make_response
from src.api.query import Query

app = Flask(__name__)

@app.route('/api/q=<query_str>', methods=['GET'])
def exec_query(query_str: str):
    # print(query_str)
    try:
        q = Query(query_str)
        return jsonify(q.send_request())
    except:
        return make_response(jsonify({'error 400': 'Bad request'}), 400)

"""
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)
"""

if __name__ == '__main__':
    app.run(debug=True)

