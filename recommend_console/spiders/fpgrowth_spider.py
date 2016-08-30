# encoding=utf8 
#scrapy crawl fpgrowth
from frequenset import UtilFrequenSet
from cnmmseg import UtilCNMmseg
from scrapy.spider import Spider
import fpgrowth
import datetime


class FpgrowthSpider(Spider):  
    name = "fpgrowth"
    start_urls = ["http://www.baidu.com"] 
        
    def parse(self, response): 
        minSup = 2
        print "###################["+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"] calculate_recommend_sets###################"
        myFreqList = UtilFrequenSet.calculate_recommend_sets(minSup)
        print len(myFreqList)
        print "###################["+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"] store_frequent_sets_by_name###################"
        UtilFrequenSet.truncate_table_data()
        UtilFrequenSet.store_frequent_sets_by_name(myFreqList)
        print "###################["+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"] calculate_search_keys###################"
        UtilCNMmseg.truncate_table_data()
        UtilCNMmseg.calculate_search_keys()
        #rows = UtilCNMmseg.get_records_by_sql("select restaurants.*,foods.* from restaurants inner join foods on restaurants.id=foods.id where 1<>1 or (foods.name like '%绵绵冰%' and foods.name like '%芒果绵绵%') order by score_times desc limit 150")
        print "###################["+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"] close mysql connection###################"
        UtilCNMmseg.close_db_connection() 
        return None
