from flask import Flask, request, jsonify
from flask_cors import CORS

import json
import requests

from pyscraper import product_scraper, query_scraper

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
        
        output = product_scraper(url)
        output = json.loads(output)
       
        return jsonify(output)

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
        query = request.args['q']
        db_url = 'https://laravel-sandbox-whattheprice.herokuapp.com/api/query/save'

        output = query_scraper(query)
        output = json.loads(output)

        if output['status_code'] == 200:
            data = {'query': query, 'user_id': user_id, 'status': output['status'], 'status_code': output['status_code'], 'result_length': output['analytics']['result_count'], 'query_time': output['elapsed_time']}
            requests.post(db_url, data=data)
        
        else:
            data = {'query': query, 'user_id': user_id, 'status': output['status'], 'status_code': output['status_code']}
            requests.post(db_url, data=data)
        
        return jsonify(output)

    else:
        return "Query not found"


if __name__ == '__main__':
    app.run(debug=True)