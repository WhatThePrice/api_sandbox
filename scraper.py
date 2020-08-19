def scraper():
    from flask import Flask, jsonify, request, make_response
    import datetime
    from scraper_api import ScraperAPIClient
    from bs4 import BeautifulSoup
    import json
    import requests
    from scipy.stats import skew
    from scipy import stats
    import numpy as np
    import statistics
    from collections import Counter
    from itertools import groupby

    saved_url = 'https://laravel-sandbox-whattheprice.herokuapp.com/api/savequery'

    user_id = None

    now = datetime.datetime.now()

    if 'user_id' in request.args:
        user_id = request.args['user_id']

    if 'q' in request.args:
        query = request.args['q']

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
            results = {"status": "OK", "status_code": "200",
                       "data": [], "analytics": []}

            xquery = query.lower().split()

            for i in range(len(data['mods']['listItems'])):
                val = []

                for j in xquery:
                    val.append(j in data['mods']
                               ['listItems'][i]['name'].lower())
                xquery_result = False if False in val else True

                if xquery_result:

                    results['data'].append({
                        "id": i,
                        "product_id": data['mods']['listItems'][i]['nid'],
                        "name": data['mods']['listItems'][i]['name'],
                        "price": float(data['mods']['listItems'][i]['price']),
                        "brand": data['mods']['listItems'][i]['brandName'],
                        "url": data['mods']['listItems'][i]['productUrl'].lstrip("//").rstrip("?search=1"),
                        "image_url": data['mods']['listItems'][i]['image'].lstrip("https://"),
                        "platform": "lazada"
                    })

            mode_price = 0
            mode_price_count = 0

            if len(results['data']) > 0:
                price = []
                for i in range(len(results['data'])):
                    price.append(results['data'][i]['price'])
                price_np = np.array(price)

                result_count = len(price)
                max_price = max(price)
                min_price = min(price)
                mean_price = round(statistics.mean(price), 2)
                median_price = statistics.median(price)
                variance = round(statistics.variance(price), 2)
                stdev = round(statistics.stdev(price), 2)
                skewness = round(skew(price_np, bias=False), 2)

                freqs = groupby(Counter(price).most_common(), lambda x: x[1])
                mode_price = [val for val, count in next(freqs)[1]]
                mode_price_count = int(str(stats.mode(price_np)[1][0]))

            else:
                result_count = 0
                max_price = 0
                min_price = 0
                mean_price = 0
                median_price = 0
                variance = 0
                stdev = 0
                skewness = 0

                mode_price = 0
                mode_price_count = 0

            results['analytics'].append({
                                        "result_count": result_count,
                                        "max_price": max_price,
                                        "min_price": min_price,
                                        "avg_price": mean_price,
                                        "median_price": median_price,
                                        "variance": variance,
                                        "stdev": stdev,
                                        "skewness": skewness,

                                        "mode_price": mode_price,
                                        "mode_price_count": mode_price_count
                                        })

            duration = (datetime.datetime.now()-now).total_seconds()

            myobj = {'query': query, 'query_time': duration, 'result_length': result_count, 'user_id': user_id,
                     'status': results['status'], 'status_code': results['status_code']}
            requests.post(saved_url, data=myobj)

        else:
            results = {"status": "Not Found",
                       "status_code": "404", "data": [], "analytics": []}
            duration = (datetime.datetime.now()-now).total_seconds()
            myobj = {'query': query, 'query_time': duration,
                     'status': results['status'], 'status_code': results['status_code']}
            requests.post(saved_url, data=myobj)

        return jsonify(results)

    else:
        results = {"status": "Bad Request",
                   "status_code": "400", "data": [], "analytics": []}
        myobj = {'query': None, 'query_time': None,
                 'status': results['status'], 'status_code': results['status_code']}
        requests.post(saved_url, data=myobj)
        return jsonify(results)
