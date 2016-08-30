#scrapy crawl shopdetail
from dianpingweb import WDPDianPingWeb
from dianpingdb import UtilDianPingDb
from scrapy.spider import Spider
from scrapy.http import Request

class ShopDetailSpider(Spider):  
    name = "shopdetail"
    allowed_domains = [WDPDianPingWeb.URL]
    start_urls = WDPDianPingWeb.get_shop_detail_search_urls()
    print "################shopdetail start_urls: %s"%(len(start_urls))
    
    def start_requests(self):
        for url in self.start_urls:   
            if url != None:      
                yield Request(url, headers={'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
                                            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                                            "Connection":"keep-alive",
                                            "Host":"www.dianping.com"})             
     
    def parse(self, response):    
        restaurant_items = WDPDianPingWeb.get_restaurant_items_from_detail_response(response)
        foods_items = WDPDianPingWeb.get_foods_items_from_detail_response(response,10)
        if restaurant_items and restaurant_items!=[]:
            UtilDianPingDb.store_restaurants_by_shop_url(restaurant_items)
        if foods_items and foods_items!=[]:
            UtilDianPingDb.store_foods_by_food_url(foods_items)
        UtilDianPingDb.close_db_connection
        print "################restaurant_items,foods_items: %s,%s"%(len(restaurant_items),len(foods_items))
        return len(restaurant_items),len(foods_items)