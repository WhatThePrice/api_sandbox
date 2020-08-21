def query_tracker():
    import requests
    import json

    url = "https://laravel-sandbox-whattheprice.herokuapp.com/api/querytracker"

    response = requests.request("GET", url)
    result = response.json()

    for i in range(len(result)):
        q = result[i]['query']
        q_id = result[i]['id']

        url = "https://api-sandbox-286406.et.r.appspot.com/api/v1/data?user_id=0&q=" + q
        url_post = "https://laravel-sandbox-whattheprice.herokuapp.com/api/savequeryprice"

        try:
            response = requests.request("GET", url)
            data = response.json()
            data_json = json.dumps(data['analytics'][0])
        except:
            data = {"status": "error"}
            data_json = json.dumps(data)

        myobj = {'query_tracker_id': q_id, 'price_analytics': data_json}
        x = requests.post(url_post, data=myobj)

        print(data_json)

    return "Success!"
