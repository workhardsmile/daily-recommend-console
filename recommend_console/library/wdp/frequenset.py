import datetime
import fpgrowth
import re,string
from database import UtilDatabase

class UtilFrequenSet(object):  
    fp_tree = None
    freq_list = None
    util_db = UtilDatabase()
    
    @classmethod
    def truncate_table_data(cls):
        #delete_sql = 'delete from ' + table_name + ' where 1=1'  
        delete_sql = 'truncate table frequent_sets'  
        cls.util_db.execute_sql(delete_sql)
        cls.util_db.commit() 
    
    @classmethod
    def close_db_connection(cls):
        cls.util_db.close_connection()
        
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
    def get_recommend_restaurants_candidacy_list(cls,min_score=None):
        if min_score==None:
            min_score=40
        select_sql = "select GROUP_CONCAT(distinct restaurant_id) from user_restaurant_configs where score>=" + str(min_score) + " group by user_id having count(restaurant_id)>0"
        cls.util_db.execute_sql(select_sql) 
        results = cls.util_db.get_rows()
        candidacy_list = []
        for result in results:
            candidacy_list.insert(len(candidacy_list),result[0].split(","))
        return candidacy_list
    
    @classmethod
    def get_unrecommend_restaurants_candidacy_list(cls,max_score=None):
        if max_score==None:
            max_score=20
        select_sql = "select GROUP_CONCAT(distinct restaurant_id) from user_restaurant_configs where score<=" + str(max_score) + " group by user_id having count(restaurant_id)>0"
        cls.util_db.execute_sql(select_sql) 
        results = cls.util_db.get_rows()
        candidacy_list = []
        for result in results:
            candidacy_list.insert(len(candidacy_list),result[0].split(","))
        return candidacy_list 
    
    @classmethod   
    def store_frequent_sets_by_name(cls,result_dicts,type=None): 
        # verify frequent_sets
        # select concat(',',group_concat(restaurant_id),',') as C from user_restaurant_configs where score=40 
        # group by user_id having C like '%,174,%' and C like '%,130,%' and C like '%,78,%';
        # select name,surport_level from frequent_sets where name like '%,174,%' and name like '%,130,%' and name like '%,78,%';
        if type==None:
            type="recommend_restaurants"
        date_now = datetime.datetime.now()
        date_str = date_now.strftime('%Y-%m-%d %H:%M:%S') 
        date_label = "chengdu" + str(date_now.year)     
        for result in result_dicts:  
            for key,value in result.iteritems():
                name = "," + cls.get_valid_value_from_str(key)+","
                select_sql = "select id from frequent_sets where name='" + name + "' and type='" + str(type) + "' and date_label='" + str(date_label) + "'"
                update_sql = "update frequent_sets set surport_level=" + str(value) + ",updated_at='"+date_str+"',last_sn=(select concat(max(id),'') as last_sn from users) where name='" + name + "' and type='" + str(type) + "' and date_label='" + str(date_label) + "'"      
                insert_sql = "insert into frequent_sets(name,surport_level,last_sn,type,date_label,created_at,updated_at) "
                insert_sql += "select %s,%s,(select concat(max(id),'') as last_sn from users),%s,%s,%s,%s"
                params = (name,str(value),str(type),str(date_label),date_str,date_str)
                cls.util_db.execute_sql(select_sql)
                if cls.util_db.row_count() > 0:
                    cls.util_db.execute_sql(update_sql)
                else:
                    cls.util_db.execute_sql(insert_sql,params)  
                         
    @classmethod
    def calculate_recommend_sets(cls,min_sup=None):
        if min_sup==None:
            min_sup=3        
        simp_data = cls.get_recommend_restaurants_candidacy_list(40)
        init_set = fpgrowth.create_init_set(simp_data)
        fp_tree, header_tab = fpgrowth.create_tree(init_set, min_sup)
        #fp_tree.disp()
        freq_list = []
        fpgrowth.mine_tree(fp_tree, header_tab, min_sup, set([]), freq_list)        
        cls.fp_tree = fp_tree
        cls.freq_list = freq_list
        return cls.freq_list
    