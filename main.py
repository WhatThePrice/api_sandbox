from flask import Flask, jsonify, request, make_response
from flask_cors import CORS

import jwt
import datetime
from functools import wraps

from scraper import scraper
import json

app = Flask(__name__)

app.config['SECRET_KEY'] = 'wh477heprices3cr3tk3y'
CORS(app)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'token is missing'}), 401

        try:
            jwt.decode(token, app.config['SECRET_KEY'])

        except:
            return jsonify({"message": "token is invalid"}), 401

        return f(*args, **kwargs)

    return decorated


@app.route('/')
def hello():
    return "Hello strangers"


@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'password':
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route('/api/v1/data', methods=['GET'])
# @token_required
def api():
    val = scraper()
    return val


@app.route('/dummy')
def dummy():
    with open("data.json", "r") as read_file:
        data = json.load(read_file)
    return data


if __name__ == '__main__':
    app.run(debug=True)
