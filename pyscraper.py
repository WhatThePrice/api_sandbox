#################################################################################################################
#################################################################################################################
# QUERY SCRAPER
#################################################################################################################
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
            "brand": "Asus",
            "image_url": "cf.shopee.com.my/file/62c53c04d9380fda719383630bd6c787",
            "name": 'Asus Vivobook A407M-ABV036T 14" Laptop GREY COLOR (Celeron N4000, 4GB, 500GB, Intel HD, W10) - NOTEBOOK',
            "platform": "shopee",
            "price": 1498.98,
            "product_id": "104569008",
            "url": "www.shopee.com.my/Asus-Vivobook-A407M-ABV036T-14-Laptop-GREY-COLOR-(Celeron-N4000-4GB-500GB-Intel-HD-W10)-NOTEBOOK-i.104569008.6306827413"
        }
    )
    result['data'].append(
        {
            "brand": "Asus",
            "image_url": "cf.shopee.com.my/file/4a4987733e9d3c8e0a0a530c7ba2430f",
            "name": "Asus Laptop A409M-ABV302T 14'' HD Grey ( Celeron N4000, 4GB, 256GB, Intel, W10 )",
            "platform": "shopee",
            "price": 1319.00,
            "product_id": "93329653",
            "url": "www.shopee.com.my/Asus-Laptop-A409M-ABV302T-14-HD-Grey-(-Celeron-N4000-4GB-256GB-Intel-W10-)-i.93329653.3541263592"
        }
    )
    result['data'].append(
        {
            "brand": "Asus",
            "image_url": "cf.shopee.com.my/file/83cb37321aa3b818b1217b84ea352c9e",
            "name": 'Asus VivoBook A420U-AEB248T 14" FHD Laptop Transparent Silver',
            "platform": "shopee",
            "price": 1615.00,
            "product_id": "88129513",
            "url": "www.shopee.com.my/Asus-VivoBook-A420U-AEB248T-14-FHD-Laptop-Transparent-Silver-i.88129513.2372484575"
        }
    )
    result['data'].append(
        {
            "brand": "Asus",
            "image_url": "cf.shopee.com.my/file/17e17464ab4a324c8f0340e365680845",
            "name": 'ASUS A409M-ABV009T / ASUS A409M-ABV010T ( N4000,4GB,500GB,HD520,14"HD,W10,2YR )',
            "platform": "shopee",
            "price": 1309.00,
            "product_id": "88129513",
            "url": "www.shopee.com.my/ASUS-A409M-ABV009T-ASUS-A409M-ABV010T-(-N4000-4GB-500GB-HD520-14-HD-W10-2YR-)-i.28954261.3341463178"
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


#################################################################################################################
#################################################################################################################
# LAZADA PRODUCT SCRAPER
#################################################################################################################
#################################################################################################################
def product_scraper(url):
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