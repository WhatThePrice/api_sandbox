def scraper():
    from flask import Flask, jsonify, request, make_response
    import datetime
    from scraper_api import ScraperAPIClient
    from bs4 import BeautifulSoup
    import json
    import requests

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

            duration = (datetime.datetime.now()-now).total_seconds()

            myobj = {'query': query, 'query_time': duration, 'user_id': user_id,
                     'status': results['status'], 'status_code': results['status_code']}
            requests.post(saved_url, data=myobj)

        else:
            results = {"status": "Not Found", "status_code": "404", "data": []}
            duration = (datetime.datetime.now()-now).total_seconds()
            myobj = {'query': query, 'query_time': duration,
                     'status': results['status'], 'status_code': results['status_code']}
            requests.post(saved_url, data=myobj)

        return jsonify(results)

    else:
        results = {"status": "Bad Request", "status_code": "400", "data": []}
        duration = (datetime.datetime.now()-now).total_seconds()
        print(duration)
        myobj = {'query': None, 'query_time': duration,
                 'status': results['status'], 'status_code': results['status_code']}
        requests.post(saved_url, data=myobj)
        return jsonify(results)
