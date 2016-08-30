#scrapy crawl shop -o dlt_items.json -t json
from dianpingweb import WDPDianPingWeb
from dianpingdb import UtilDianPingDb
from scrapy.spider import Spider
from scrapy.http import Request

class ShopSpider(Spider):  
    name = "shop"
    html_dict={'name':'restaurants','value':'r1577'}
    allowed_domains = [WDPDianPingWeb.URL]
    start_urls = WDPDianPingWeb.get_shop_search_urls_by_dict(html_dict['value'],50)
    print "################shop start_urls: %s"%(len(start_urls))
    #UtilDianPingDb.truncate_table_data(html_dict['name'])
    
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, headers={'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
                                        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                                        "Connection":"keep-alive",
                                        "Host":"www.dianping.com"}) 
     
    def parse(self, response):   
        restaurant_items,food_items = WDPDianPingWeb.get_restaurant_and_food_items_from_response(response)
        if restaurant_items and restaurant_items!=[]:
            UtilDianPingDb.store_restaurants_by_shop_url(restaurant_items)           
        if food_items and food_items!=[]:
            UtilDianPingDb.store_foods_by_food_url(food_items)
        UtilDianPingDb.close_db_connection
        print "################restaurant_items,food_items: %s,%s"%(len(restaurant_items),len(food_items))
        return len(restaurant_items),len(food_items)