#scrapy crawl member
from dianpingweb import WDPDianPingWeb
from dianpingdb import UtilDianPingDb
from scrapy.spider import Spider
from scrapy.http import Request

class MemberSpider(Spider):  
    name = "member"
    allowed_domains = [WDPDianPingWeb.URL]
    start_urls = WDPDianPingWeb.get_member_recommend_search_urls(50)
    print "################member start_urls: %s"%(len(start_urls))
    
    def start_requests(self):
        for url in self.start_urls:        
            yield Request(url, headers={'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0",
                                        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                                        "Connection":"keep-alive",
                                        "Host":"www.dianping.com"})            
     
    def parse(self, response):    
        user_restaurant_items = WDPDianPingWeb.get_user_restaurant_items_from_detail_response(response)
        if user_restaurant_items and user_restaurant_items!=[]:
            UtilDianPingDb.store_user_restaurants_by_id(user_restaurant_items)
            UtilDianPingDb.close_db_connection
        print "################user_restaurant_items: %s"%(len(user_restaurant_items))
        return len(user_restaurant_items)