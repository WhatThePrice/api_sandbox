#################################################################################################################
# QUERY SCRAPER
#################################################################################################################
def query_scraper(query):
    from scraper_api import ScraperAPIClient
    from bs4 import BeautifulSoup
    import json
    import statistics

    ##################################################################
    # LAZADA SCRAPER STARTS HERE
    ##################################################################
    url = 'https://www.lazada.com.my/catalog/?q=' + query

    xquery = query.lower().split()

    client = ScraperAPIClient('9aa1dbc863b8334850efccb9be3552f8')

    try:
        page = client.get(url=url, render=True)
    except:
        result = {'status_code': 500, 'status': 'scraper api fatal error',
                  'elapsed_time': '', 'data': [], 'analytics': {}}
        return json.dumps(result)

    if page.status_code != 200:
        result = {'status_code': page.status_code, 'status': 'error',
                  'elapsed_time': int(page.elapsed.total_seconds()), 'data': [], 'analytics': {}}
        return json.dumps(result)

    else:
        soup = BeautifulSoup(page.content, 'html.parser')
        scripts = soup.find_all('script')

        if not scripts:
            result = {'status_code': 500, 'status': 'no script tag found',
                      'elapsed_time': int(page.elapsed.total_seconds()), 'data': [], 'analytics': {}}
            return json.dumps(result)

        else:
            data = None
            for i in range(len(scripts)):
                if "<script>window.pageData=" in str(scripts[i]):
                    data = str(scripts[i]).lstrip(
                        "<script>window.pageData=").rstrip("</script>")
                    data = json.loads(data)

            if data == None:
                result = {'status_code': 500, 'status': 'no window.pagedata found',
                          'elapsed_time': int(page.elapsed.total_seconds()), 'data': [], 'analytics': {}}
                return json.dumps(result)

            else:
                if "listItems" not in data['mods']:
                    result = {'status_code': 400, 'status': 'no listItems found',
                              'elapsed_time': int(page.elapsed.total_seconds()), 'data': [], 'analytics': {}}
                    return json.dumps(result)

                else:
                    result = {'status_code': 200, 'status': 'success',
                              'elapsed_time': int(page.elapsed.total_seconds()), 'data': [], 'analytics': {}}

                    for i in range(len(data['mods']['listItems'])):
                        val = []

                        for j in xquery:
                            val.append(j in data['mods']
                                       ['listItems'][i]['name'].lower())
                            xquery_result = False if False in val else True

                        if xquery_result:
                            result['data'].append({
                                "product_id": data['mods']['listItems'][i]['nid'],
                                "name": data['mods']['listItems'][i]['name'],
                                "price": float(data['mods']['listItems'][i]['price']),
                                "brand": data['mods']['listItems'][i]['brandName'],
                                "url": data['mods']['listItems'][i]['productUrl'].lstrip("//").rstrip("?search=1"),
                                "image_url": data['mods']['listItems'][i]['image'].lstrip("https://"),
                                "platform": "lazada"
                            })

    ##################################################################
    # SHOPEE SCRAPER STARTS HERE
    ##################################################################
    result['data'].append(
        {
            "brand": "Nike",
            "image_url": "https://cf.shopee.com.my/file/3e6e90a6949afd32de89891ac82726a9",
            "name": 'ASUS TUF Gaming FX505D-TAL409T - AMD Ryzen™ 7-3750H | 4GB RAM | 512GB SSD | GTX1650 4GB | 15.6" FHD 120Hz',
            "platform": "shopee",
            "price": 3071.04,
            "product_id": "999999999999",
            "url": "https://shopee.com.my/ASUS-TUF-Gaming-FX505D-TAL409T-AMD-Ryzen%E2%84%A2-7-3750H-4GB-RAM-512GB-SSD-GTX1650-4GB-15.6-FHD-120Hz-i.96894599.6436369259"
        }
    )
    result['data'].append(
        {
            "brand": "Nike",
            "image_url": "https://cf.shopee.com.my/file/87fa4fd209653fb7df248030acdfba7b",
            "name": "【Shopee Mall】 Original TWS inPods 12 Wireless Earphone Bluetooth Colorful HiFi Sports Earbud",
            "platform": "shopee",
            "price": 22,
            "product_id": "8888888888888888",
            "url": "https://shopee.com.my/%E3%80%90Shopee-Mall%E3%80%91-Original-TWS-inPods-12-Wireless-Earphone-Bluetooth-Colorful-HiFi-Sports-Earbud-i.159892917.4001820259"
        }
    )
    ##################################################################
    # RENUMBERED ID LIST
    for i in range(len(result['data'])):
        result['data'][i]['id'] = i+1
    ##################################################################

    if len(result['data']) < 1:
        result = {'status_code': 400, 'status': 'no matched result',
                  'elapsed_time': int(page.elapsed.total_seconds()), 'data': [], 'analytics': {}}
        return json.dumps(result)

    else:
        price = []
        for i in range(len(result['data'])):
            price.append(result['data'][i]['price'])

        result['analytics']['result_count'] = len(price)
        result['analytics']['max_price'] = max(price)
        result['analytics']['min_price'] = min(price)
        result['analytics']['avg_price'] = round(statistics.mean(price), 2)
        result['analytics']['median_price'] = statistics.median(price)
        result['analytics']['min_price_url'] = result['data'][price.index(
            min(price))]['url']

        return json.dumps(result)


# Main query scraper function with retry function.
def query_retry(query, user_id, retry=3):
    import json
    import requests

    new_elapsed_time = 0
    for i in range(retry):
        output = json.loads(query_scraper(query))
        if output['status'] != 'scraper api fatal error':
            new_elapsed_time += output['elapsed_time']
            break
        else:
            print('try:', str(i+1))
            new_elapsed_time += output['elapsed_time']

    output['retry'] = i
    output['elapsed_time'] = new_elapsed_time

    db_url = 'https://laravel-sandbox-whattheprice.herokuapp.com/api/query/save'
    myobj = {'query': query, 'user_id': user_id,
             'status': output['status'], 'status_code': output['status_code'], 'result_length': output['analytics']['result_count'], 'query_time': output['elapsed_time']}
    requests.post(db_url, data=myobj)

    return output


#################################################################################################################
# LAZADA PRODUCT SCRAPER
#################################################################################################################

# Core lazada product scraper function.
def lazada_product_scraper(url):
    from scraper_api import ScraperAPIClient
    from bs4 import BeautifulSoup
    import json

    client = ScraperAPIClient('9aa1dbc863b8334850efccb9be3552f8')

    try:
        page = client.get(url=url, render=True)
    except:
        result = {'status_code': 500, 'status': 'scraper api fatal error',
                  'elapsed_time': '', 'price': '', 'title': ''}
        return json.dumps(result)

    if page.status_code != 200:
        result = {'status_code': page.status_code, 'status': 'error',
                  'elapsed_time': int(page.elapsed.total_seconds()), 'price': '', 'title': ''}
        return json.dumps(result)

    else:
        soup = BeautifulSoup(page.content, 'html.parser')
        result_title = soup.findAll(
            "span", {"class": "pdp-mod-product-badge-title"})
        result_price = soup.findAll("div", {"class": "pdp-product-price"})

        if result_title and result_price:
            title = result_title[0].text
            price = float(result_price[0].find_next(
                'span').text.strip('RM').replace(',', ''))

            result = {'status_code': page.status_code, 'status': 'success', 'elapsed_time': int(
                page.elapsed.total_seconds()), 'title': title, 'price': price}
            return json.dumps(result)

        else:
            result = {'status_code': 500, 'status': 'blocked/nocontent',
                      'elapsed_time': int(page.elapsed.total_seconds()), 'title': '', 'price': ''}
            return json.dumps(result)


# Main lazada product scraper function with retry function.
def lazada_product_retry(url, retry=3):
    import json
    new_elapsed_time = 0
    for i in range(retry):
        output = json.loads(lazada_product_scraper(url))
        if output['status'] != 'blocked/nocontent':
            new_elapsed_time += output['elapsed_time']
            output['retry'] = i
            break
        else:
            print('try:', str(i+1))
            new_elapsed_time += output['elapsed_time']
            output['retry'] = i

    output['elapsed_time'] = new_elapsed_time
    return output


#################################################################################################################
# SHOPEE PRODUCT SCRAPER
#################################################################################################################

# Core shopee product scraper function.
def product_shopee_scraper(url):
    return 'In progress'


# Main shopee product scraper function with retry function.
def main_shopee(url, retry=3):
    return 'In progress'
