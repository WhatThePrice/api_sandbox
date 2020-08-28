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
    print('save_query_price', result)