from flask import Flask, jsonify, request
from flask_cors import CORS

import json
import requests

from pyscraper import lazada_product_retry, query_retry

app = Flask(__name__)

CORS(app)


@app.route('/')
def home():
    return "You lost, stranger?"


# /////////////////////////////////////////////////Product Scraper Function//////////////////////////////
@app.route('/api/scraper/product', methods=['GET'])
def productlazada():
    if 'url' in request.args:
        url = request.args['url']
        return lazada_product_retry(url)
    else:
        return "URL not found"


# /////////////////////////////////////////////////Query Scraper Function//////////////////////////////
@app.route('/api/scraper/query', methods=['GET'])
def queryscraper():
    if 'user_id' in request.args:
        user_id = request.args['user_id']
    else:
        user_id = 0
    if 'q' in request.args:
        try:
            query = request.args['q']
            return query_retry(query, user_id)
        except:
            return json.dumps({'status':'server error', 'status_code':500})
    else:
        return "Query not found"


if __name__ == '__main__':
    app.run(debug=True)
