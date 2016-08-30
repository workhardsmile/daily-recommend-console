# encoding=utf8 
import datetime
import re,string
from database import UtilDatabase
import mmseg

class UtilCNMmseg(object):  
    fp_tree = None
    freq_list = None
    util_db = UtilDatabase()
    mmseg.Dictionary.load_dictionaries()
    
    @classmethod
    def truncate_table_data(cls):
        #delete_sql = 'delete from ' + table_name + ' where 1=1'  
        delete_sql = 'truncate table search_keys'  
        cls.util_db.execute_sql(delete_sql) 
    
    @classmethod
    def close_db_connection(cls):
        cls.util_db.close_connection()
        
    @classmethod
    def get_records_by_sql(cls,sql):
        cls.util_db.execute_sql(sql)
        return cls.util_db.get_rows()
        
    @classmethod   
    def get_valid_value_from_str(cls,str_data):
        #str_data = str_data.encode('utf-8')
        if str_data==None: 
            str_data = ""
        else:
            str_data = str(str_data)
        try:
            pattern = r"u\'(.+?)\'"
            matchs = re.findall(pattern,str_data)
            temp = ""
            for match in matchs:
                if match:
                    temp += "," + match 
            if temp!= "": str_data = temp[1:]
        except Exception, e:
            print "Exception: %s in %s" % (e, str_data)
        return str_data.replace("\n","").replace("\r", "").strip()
        
    @classmethod   
    def store_search_keys_by_name(cls,names_list,table_column,type=None): 
        if type==None:
            type="foods"
        date_now = datetime.datetime.now()
        date_str = date_now.strftime('%Y-%m-%d %H:%M:%S')    
        for result in names_list:  
            for key,value in result.iteritems():
                name = cls.get_valid_value_from_str(key)
                select_sql = "select id from search_keys where name='" + name + "' and type='" + str(type) + "' and params='" + str(table_column) + "' and start_index=" + str(value[0]) + " and end_index=" + str(value[1])    
                insert_sql = "insert into search_keys(name,start_index,end_index,params,type,created_at,updated_at) values(%s,%s,%s,%s,%s,%s,%s)"
                params = (name,value[0],value[1],str(table_column),str(type),date_str,date_str)
                cls.util_db.execute_sql(select_sql)
                if cls.util_db.row_count() < 1:
                    cls.util_db.execute_sql(insert_sql,params) 
                
    @classmethod
    def get_mmseg_list_from_data_str(cls,str_data):
        mmseg_list=[]
        row = cls.get_valid_value_from_str(str_data)
        if str(row).strip()!="":
            try:
                algor = mmseg.Algorithm(row)
                for tok in algor:
                    if str(tok.text).strip()!="": mmseg_list.insert(len(mmseg_list),{tok.text:[tok.start,tok.end]})
            except Exception, e:
                print e
        return mmseg_list
                
    @classmethod   
    def calculate_search_keys(cls):
        #foods
        food_names_list = []
        restaurant_names_list = []
        types_list = []
        #location_list = []
        address_list = []
        level_list = []
        comment_list = []
        select_sql = "select foods.name from foods where 1=1"
        cls.util_db.execute_sql(select_sql)
        if cls.util_db.row_count() > 0:
            data_rows = cls.util_db.get_rows()
            for row in data_rows:
                food_names_list += cls.get_mmseg_list_from_data_str(row[0])
        cls.store_search_keys_by_name(food_names_list, 'foods.name', 'foods')
        #restaurants
        select_sql = "select restaurants.name, restaurants.type, restaurants.location, restaurants.address, restaurants.level, restaurants.comment from restaurants where 1=1"
        cls.util_db.execute_sql(select_sql)
        if cls.util_db.row_count() > 0:
            data_rows = cls.util_db.get_rows()
            for row in data_rows:
                restaurant_names_list += cls.get_mmseg_list_from_data_str(str(row[0]).replace(str(row[2]),""))
                types_list += cls.get_mmseg_list_from_data_str(row[1])
                #location_list += cls.get_mmseg_list_from_data_str(row[2])
                address_list += cls.get_mmseg_list_from_data_str(row[3])                
                level_list += cls.get_mmseg_list_from_data_str(row[4])
                comment_list += cls.get_mmseg_list_from_data_str(row[5])
        cls.store_search_keys_by_name(restaurant_names_list, 'restaurants.name', 'restaurants')
        cls.store_search_keys_by_name(types_list, 'restaurants.type', 'restaurants')
        #cls.store_search_keys_by_name(location_list, 'restaurants.location', 'restaurants')
        cls.store_search_keys_by_name(address_list, 'restaurants.address', 'restaurants')        
        cls.store_search_keys_by_name(level_list, 'restaurants.level', 'restaurants')
        cls.store_search_keys_by_name(comment_list, 'restaurants.comment', 'restaurants')
        create_sql = "CREATE TABLE IF NOT EXISTS t_temp as select name from search_keys where params='restaurants.location' or params='restaurants.address' or params='restaurants.level' or params='restaurants.comment'"
        cls.util_db.execute_sql(create_sql)
        delete_sql = "delete from search_keys where name in (select name from t_temp) and params='restaurants.name'"
        cls.util_db.execute_sql(delete_sql)
    