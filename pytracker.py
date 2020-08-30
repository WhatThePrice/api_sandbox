#/////////////////////////////////////////////////////////////////////////////
# QUERY TRACKER
#/////////////////////////////////////////////////////////////////////////////
def get_query_list():
    import requests
    import json
    url = 'https://laravel-sandbox-whattheprice.herokuapp.com/api/tracker/query/list'
    result = requests.get(url)
    output = json.loads(result.text)['query_list']
    return output

def save_query_price(id, price):
    import requests
    url = 'https://laravel-sandbox-whattheprice.herokuapp.com/api/price/query/save'
    data = {'query_tracker_id': id, 'price_analytics': price}
    result = requests.post(url, data = data)

def track_query_price():
    import requests
    import json

    output = get_query_list()

    for i in range(len(output)):
        query = output[i]['query']
        tracker_id = output[i]['id']

        url = 'https://api-sandbox-286406.et.r.appspot.com/api/scraper/query?q=' + query  + '&user_id=0'
        result = requests.get(url)

        if json.loads(result.text)['status_code'] != 200:
            price = {'result_count': 0}
            save_query_price(tracker_id, json.dumps(price))

        else:
            price = json.loads(result.text)['analytics']
            save_query_price(tracker_id, json.dumps(price))

    return 'Complete.'
#/////////////////////////////////////////////////////////////////////////////
# PRODUCT TRACKER
#/////////////////////////////////////////////////////////////////////////////
def get_product_list():
    import requests
    import json
    url = 'https://laravel-sandbox-whattheprice.herokuapp.com/api/tracker/product/list'
    result = requests.get(url)
    output = json.loads(result.text)['product_list']
    return output

def save_product_price(id, price):
    import requests
    url = 'https://laravel-sandbox-whattheprice.herokuapp.com/api/price/product/save'
    data = {'product_tracker_id': id, 'price': price}
    result = requests.post(url, data = data)

def track_product_price():
    import requests
    import json

    output = get_product_list()

    for i in range(len(output)):
        product_url = output[i]['product_url']
        tracker_id = output[i]['id']

        url = 'https://api-sandbox-286406.et.r.appspot.com/api/scraper/product?url=' + product_url
        result = requests.get(url)

        price = json.loads(result.text)['price']

        save_product_price(tracker_id, price)

    return 'Complete.'