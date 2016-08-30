# encoding=utf8 
import re,string
from dpitems import UserItem,RestaurantItem,FoodItem,UserRestaurantItem
from scrapy.selector import Selector
from dianpingdb import UtilDianPingDb
from scrapy.http import HtmlResponse

class WDPDianPingWeb(object):
    URL = 'http://www.dianping.com'
    @classmethod
    def get_shop_search_urls_by_dict(cls,html_value,max_page=None): 
        if max_page==None:
            max_page=10
        search_urls = []
        for i in range(max_page):           
            search_url = cls.URL + '/search/category/8/10/' + html_value + 'p' + str(i+1)
            search_urls.insert(len(search_urls), search_url)
        return search_urls
    @classmethod
    def get_valid_value_from_data(cls,data_list):
        #str_data = str_data.encode('utf-8')
        str_data = ""
        try:    
            if  data_list==None or data_list==[]:
                data_list=['']          
            str_data = "".join([t.encode('utf-8') for t in data_list])
            pattern = r"u\'(.+?)\'"
            matchs = re.findall(pattern,str_data)
            temp = ""
            for match in matchs:
                if match:
                    temp += "," + match 
            if temp!= "": str_data = temp[1:]
        except Exception, e:
            print "Exception: %s in %s" % (e, data_list)
        return str_data.replace("\n","").replace("\r", "").strip()
    @classmethod
    def get_user_urls_from_db(cls):
        UtilDianPingDb.get_db_columnss('user_url','users',{})
    @classmethod
    def get_shop_urls_from_db(cls):
        UtilDianPingDb.get_db_columnss('shop_url','restaurants',{})
    @classmethod
    def get_restaurant_and_food_items_from_response(cls,response):
        selector = Selector(response)
        sites = selector.xpath("//ul[@class='shop-list J_shop-list']/li")  
        restaurant_items = [] 
        food_items = [] 
        if sites:
            for tr in sites: 
                item = RestaurantItem()
                item['name'] = cls.get_valid_value_from_data(tr.xpath(".//div[@class='info']//p[@class='title']//a[1][@class='shopname']//span[1]").xpath('text()').extract())
                item['type'] = cls.get_valid_value_from_data(tr.xpath(".//div[@class='message']//p[@class='address']//a[contains(@href,'/g')][1]").xpath('text()').extract())
                item['location'] = cls.get_valid_value_from_data(tr.xpath(".//div[@class='message']//p[@class='address']//a[contains(@href,'/r')][1]").xpath('text()').extract())
                item['price'] = cls.get_valid_value_from_data(tr.xpath(".//div[@class='info']//p[@class='comment']//span[@class='price']").xpath('text()').extract())
                item['level'] = cls.get_valid_value_from_data(tr.xpath(".//div[@class='info']//p[@class='remark']//span[contains(@class,'sml-rank-stars')]").xpath('@title').extract())
                item['shop_url'] = cls.URL + cls.get_valid_value_from_data(tr.xpath(".//a[1]").xpath("@href").extract())
                item['image_url'] = cls.get_valid_value_from_data(tr.xpath(".//a[1]//img[contains(@data-src,'')][1]").xpath("@data-src").extract())
                item['scores'] = cls.get_valid_value_from_data(tr.xpath(".//div[@class='info']//p[@class='comment']//span[@class='comment-list']").xpath('text()').extract())
                item['score_times'] = cls.get_valid_value_from_data(tr.xpath(".//div[@class='info']//p[@class='remark']//span//a[contains(@href,'#comment')][1]").xpath('text()').extract())
                tds = tr.xpath(".//div[@class='info']/a[contains(@class,'tuan')]")
                comment = ""
                if tds:
                    for td in tds:
                        comment += cls.get_valid_value_from_data(td.xpath('text()').extract())
                item['comment'] = comment
                item['score_times'] = str(item['score_times']).strip().replace("封点评","")
                if item['score_times']=="" or item['score_times']=="-": item['score_times']='0'
                restaurant_items.insert(len(restaurant_items),item)
                foods=tr.xpath(".//div[@class='message']//p[@class='menu']//a")
                if foods:
                    for food in foods:
                        food_item = FoodItem()
                        food_item['food_url'] = cls.URL + cls.get_valid_value_from_data(food.css('::attr(href)').extract())
                        food_item['recommend_times'] = cls.get_valid_value_from_data(food.css('::attr(title)').extract())
                        food_item['name'] = cls.get_valid_value_from_data(food.css('::text').extract())
                        food_item['image_url'] = "[shop]" + item['shop_url']
                        food_item['recommend_times'] = str(food_item['recommend_times']).strip().replace("人推荐","")
                        if food_item['recommend_times']=="": food_item['recommend_times']='0'
                        food_items.insert(len(food_items), food_item)                     
        return restaurant_items,food_items
    @classmethod
    def get_shop_detail_search_urls(cls): 
        search_urls = []        
        shop_urls = UtilDianPingDb.get_db_records("restaurants",{},['shop_url'])
        for shop_url in shop_urls:           
            search_urls.insert(len(search_urls), shop_url[0])
        return search_urls
    @classmethod
    def get_food_detail_search_urls(cls): 
        search_urls = []        
        shop_urls = UtilDianPingDb.get_db_records("foods",{},['food_url'])
        for shop_url in shop_urls:           
            search_urls.insert(len(search_urls), shop_url[0])
        return search_urls
    @classmethod
    def get_member_recommend_search_urls(cls,max_num=None):
        if max_num==None:
            max_num=15   
        search_urls = []        
        shop_urls = UtilDianPingDb.get_db_records("restaurants",{},['shop_url','score_times'])
        for shop_url in shop_urls: 
            page_no = int(shop_url[1])/20
            if page_no > max_num: page_no = max_num
            for i in range(page_no):           
                search_urls.insert(len(search_urls),shop_url[0]+"/review_all?pageno="+str(i+1))
        return search_urls
    @classmethod
    def get_restaurant_items_from_detail_response(cls,response):
        if response.url==None or response.url==[]:
            return None
        shop_url = response.url
        selector = Selector(response)
        restaurant_item = RestaurantItem()
        restaurant_item['address'] =  cls.get_valid_value_from_data(selector.xpath("//div[@class='expand-info address']//span[@itemprop='street-address']").xpath('text()').extract()) 
        restaurant_item['telephone'] =  cls.get_valid_value_from_data(selector.xpath("//*[@class='expand-info tel']//span[@itemprop='tel']").xpath('text()').extract()) 
        restaurant_item['shop_url'] =  shop_url        
        return [restaurant_item]
    @classmethod
    def get_foods_items_from_detail_response(cls,response,max_num=None):    
        if max_num==None:
            max_num=5   
        if response.url==None or response.url==[]:
            return None
        shop_url = response.url
        shop_ids = UtilDianPingDb.get_db_records("restaurants",{'shop_url': shop_url},['id'])
        if len(shop_ids) < 1:
            return None  
        #pattern = r"<a.+href=\"(/.+dish.+)\".+title\=\"(.+)\".+<em.+class=\"count\">\([0-9]+\)</em>"  
        #sites = selector.xpath("//div[@id='shop-tabs']//p[@class='recommend-name']/a")       
        selector = Selector(response)
        sites = selector.xpath("//a[contains(@href,'dish')]")
        count = 0
        foods_items=[]
        for tr in sites:      
            food_item = FoodItem()
            food_item["restaurant_id"] = shop_ids[0][0]
            food_item["name"] = cls.get_valid_value_from_data(tr.css("::text").extract()) 
            food_item["food_url"] = cls.get_valid_value_from_data(tr.css("a::attr(href)").extract())
            #food_item["recommend_times"] = cls.get_valid_value_from_data(tr.css("span::text").extract())
            #food_item["price"] = cls.get_valid_value_from_data(tr.css("span::text").extract())            
            #food_item["image_url"] = cls.get_valid_value_from_data(tr.css("img::attr(src)").extract())             
            if not food_item in foods_items:
                foods_items.insert(len(foods_items),food_item)
                count += 1           
            if count>=max_num:
                break
        return foods_items
    @classmethod
    def get_food_items_from_food_response(cls,response):  
        selector = Selector(response)
        food_item = FoodItem()  
        food_item['food_url'] = response.url
        try: 
            food_item['price'] = cls.get_valid_value_from_data(selector.xpath("//div[@class='dish-name']//span[@class='dish-price']").css("::text").extract())        
        except Exception,e:
            food_item['price'] = "-"
        try: 
            food_item['image_url'] = cls.get_valid_value_from_data(selector.xpath("//ul[1]/li[1]//img[1]").xpath("@src").extract())        
        except Exception,e:
            food_item['image_url'] = ""
        return [food_item]
    @classmethod
    def get_user_restaurant_items_from_detail_response(cls,response):
        if response.url==None or response.url==[]:
            return None
        shop_url = response.url.split("/review_all")[0]
        selector = Selector(response)
        sites = selector.xpath("//div[@class='comment-list']//ul/li")
        user_restaurant_items = []
        if sites:
            for tr in sites:
                user_item = UserItem()
                user_restaurant_item = UserRestaurantItem()
                user_item["name"] = cls.get_valid_value_from_data(tr.css('div[class*=pic] p[class*=name] a::text').extract()) 
                user_item["user_url"] = cls.URL + cls.get_valid_value_from_data(tr.css('div[class*=pic] p[class*=name] a::attr(href)').extract()) 
                UtilDianPingDb.store_users_by_user_url([user_item])
                user_ids = UtilDianPingDb.get_db_records("users",{'user_url': user_item["user_url"]},['id'])
                shop_ids = UtilDianPingDb.get_db_records("restaurants",{'shop_url': shop_url},['id'])
                if len(user_ids) < 1 or len(shop_ids) < 1:
                    continue
                user_restaurant_item["user_id"] = user_ids[0][0]
                user_restaurant_item["restaurant_id"] = shop_ids[0][0]
                user_restaurant_item["score"] = cls.get_valid_value_from_data(tr.css('div[class*=content] div[class*=user-info] span[class*=item-rank-rst]::attr(class)').extract())[-2:]
                user_restaurant_item["comment"] = cls.get_valid_value_from_data(tr.css('div[class*=content] div[class*=comment-txt] div[class*=J_brief-cont]::text').extract())
                user_restaurant_items.insert(len(user_restaurant_items),user_restaurant_item)
                
        return user_restaurant_items