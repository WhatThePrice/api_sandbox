from flask import Flask, jsonify, request, make_response
import jwt
import datetime
from functools import wraps

from scraper_api import ScraperAPIClient
from bs4 import BeautifulSoup
import json

from foo import bar

app = Flask(__name__)

app.config['SECRET_KEY'] = 'wh477heprices3cr3tk3y'


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
    return bar()


@app.route('/close')
@token_required
def close():
    return jsonify({'message': 'for registered users only'})


@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'password':
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route('/api/v1/data', methods=['GET'])
@token_required
def api():

    if 'q' in request.args:
        query = request.args['q']
        now = datetime.datetime.now()

        url = 'https://www.lazada.com.my/catalog/?q=' + query
        client = ScraperAPIClient('c9ec9794c69af3279d1c3664445b4a79')
        page = client.get(url=url, render=True)

        soup = BeautifulSoup(page.content, 'html.parser')
        scripts = soup.find_all('script')

        for i in range(len(scripts)):
            if "<script>window.pageData=" in str(scripts[i]):
                data = str(scripts[i]).lstrip(
                    "<script>window.pageData=").rstrip("</script>")
                data = json.loads(data)

        if "listItems" in data['mods']:
            len(data['mods']['listItems'])
            results = {"status": "OK", "status_code": "200", "data": []}

            xquery = query.lower().split()

            for i in range(len(data['mods']['listItems'])):
                val = []

                for j in xquery:
                    val.append(j in data['mods']
                               ['listItems'][i]['name'].lower())
                xquery_result = False if False in val else True

                if xquery_result:

                    results['data'].append({
                        "product_id": data['mods']['listItems'][i]['nid'],
                        "name": data['mods']['listItems'][i]['name'],
                        "price": float(data['mods']['listItems'][i]['price']),
                        "brand": data['mods']['listItems'][i]['brandName'],
                        "url": data['mods']['listItems'][i]['productUrl'].lstrip("//").rstrip("?search=1"),
                        "image_url": data['mods']['listItems'][i]['image'].lstrip("https://")
                    })
        else:
            print("Search No Result")
            results = {"status": "Not Found", "status_code": "404", "data": []}

        duration = (datetime.datetime.now()-now).total_seconds()

        return jsonify(results)

    else:
        results = {"status": "Bad Request", "status_code": "400", "data": []}
        return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
