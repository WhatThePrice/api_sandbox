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
            "brand": "Acer",
            "image_url": "cf.shopee.com.my/file/a62d7af1dba88fd9fa282095fff52c59",
            "name": 'ACER ED272A 27" IPS FHD LED LCD DVI,HDMI MONITOR [ FREE HDMI CABLE ]',
            "platform": "shopee",
            "price": 519,
            "product_id": "20108462",
            "url": "www.shopee.com.my/ACER-ED272A-27-IPS-FHD-LED-LCD-DVI-HDMI-MONITOR-FREE-HDMI-CABLE--i.20108462.5916278598"
        }
    )
    result['data'].append(
        {
            "brand": "Xiaomi",
            "image_url": "cf.shopee.com.my/file/442429847411be6d7ca426252cbdb9ec",
            "name": "Xiaomi Mi Surface 34-inch Curved Gaming Monitor Screen 24:9 144Hz High Refresh Rate 1500R Curvature Computer Game Monit",
            "platform": "shopee",
            "price": 2049.20,
            "product_id": "252003586",
            "url": "www.shopee.com.my/Xiaomi-Mi-Surface-34-inch-Curved-Gaming-Monitor-Screen-24-9-144Hz-High-Refresh-Rate-1500R-Curvature-Computer-Game-Monit-i.252003586.6541469139"
        }
    )
    result['data'].append(
        {
            "brand": "Samsung",
            "image_url": "cf.shopee.com.my/file/a2d40da701ba80de8927f26a9e3201d4",
            "name": 'Samsung LC24F390FHEXXM 24" 16:9 1920 x 1080 Full HD 60Hz Monitor SF350 with Slim Depth Design (LED, HDMI, VGA)',
            "platform": "shopee",
            "price": 386,
            "product_id": "93329653",
            "url": "www.shopee.com.my/Samsung-LC24F390FHEXXM-24-16-9-1920-x-1080-Full-HD-60Hz-Monitor-SF350-with-Slim-Depth-Design-(LED-HDMI-VGA)-i.93329653.3316219469"
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