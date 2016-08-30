import datetime
from database import UtilDatabase

class UtilDianPingDb(object):
    util_db = UtilDatabase()
    
    @classmethod
    def truncate_table_data(cls,table_name):
        #delete_sql = 'delete from ' + table_name + ' where 1=1'  
        delete_sql = 'truncate table ' + table_name  
        cls.util_db.execute_sql(delete_sql)  
        
    @classmethod
    def insert_table_results(cls,table_name,results):
        date_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')         
        for result in results:           
            insert_sql = 'insert into ' + table_name + '('
            values = 'values('
            for key,value in result.iteritems(): 
                #delete_sql += key + '=%s' + ' and '                    
                insert_sql += key + ' ,'
                values += '%s ,'
            insert_sql = insert_sql + 'created_at, updated_at) ' + values + "%s, %s)"
            #insert_sql = insert_sql[:-2] + ") " + values[:-2]+")"
            params = tuple(result.values())+(date_str,date_str)
            cls.util_db.execute_sql(insert_sql,params)
 
    @classmethod
    def get_db_records(cls,table_name,conditions=None,columns=None):
        if conditions==None:
            conditions={}
        if columns==None:
            columns=[]
        colstr = "*" 
        if columns and str(columns) > 1:
            colstr = ",".join(columns)
        elif columns and str(columns) > 1:
            colstr = columns[0]
        select_sql = 'select ' + colstr + ' from ' + table_name + ' where '
        for key,value in conditions.iteritems(): 
            select_sql += key + '=%s' + ' and '                    
        select_sql += '1=1'
        params = tuple(conditions.values())
        cls.util_db.execute_sql(select_sql,params) 
        results = cls.util_db.get_rows()
        return results
    
    @classmethod
    def store_restaurants_by_shop_url(cls,results): 
        date_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')         
        for result in results:
            if 'name' in result.keys() and str(result["name"])=="":
                continue  
            select_sql = "select id from restaurants where shop_url='" + result['shop_url'] + "'"
            update_sql = 'update restaurants set '       
            insert_sql = 'insert into restaurants('
            values = 'values('
            for key,value in result.iteritems(): 
                update_sql += key + "='" + str(value).replace("'","") + "', "                    
                insert_sql += key + ', '
                values += '%s ,'
            update_sql += "updated_at='"+date_str+"' where shop_url='" + result['shop_url'] +"'"
            insert_sql = insert_sql + 'created_at, updated_at) ' + values + "%s, %s)"
            #insert_sql = insert_sql[:-2] + ") " + values[:-2]+")"
            params = tuple(result.values())+(date_str,date_str)
            cls.util_db.execute_sql(select_sql)
            if cls.util_db.row_count() > 0:
                cls.util_db.execute_sql(update_sql)
            else:
                cls.util_db.execute_sql(insert_sql,params)

    @classmethod
    def store_users_by_user_url(cls,results):
        date_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')         
        for result in results:  
            if 'name' in result.keys() and str(result["name"])=="":
                continue
            select_sql = "select id from users where user_url='" + result['user_url'] + "'"
            update_sql = 'update users set '       
            insert_sql = 'insert into users('
            values = 'values('
            for key,value in result.iteritems(): 
                update_sql += key + "='" + str(value).replace("'","") + "', "                    
                insert_sql += key + ', '
                values += '%s ,'
            update_sql += "updated_at='"+date_str+"' where user_url='" + result['user_url'] +"'"
            insert_sql = insert_sql + 'created_at, updated_at) ' + values + "%s, %s)"
            #insert_sql = insert_sql[:-2] + ") " + values[:-2]+")"
            params = tuple(result.values())+(date_str,date_str)
            cls.util_db.execute_sql(select_sql)
            if cls.util_db.row_count() > 0:
                cls.util_db.execute_sql(update_sql)
            else:
                cls.util_db.execute_sql(insert_sql,params)
                
    @classmethod   
    def store_foods_by_food_url(cls,results):
        date_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')         
        for result in results: 
            if 'name' in result.keys() and str(result["name"])=="":
                continue 
            if 'image_url' in result.keys() and result['image_url'].startswith("[shop]"):
                shop_url = result['image_url'].replace("[shop]","")
                shop_ids = cls.get_db_records("restaurants",{'shop_url': shop_url},['id'])
                if len(shop_ids) < 1:
                    return None
                else:
                    result['restaurant_id'] = shop_ids[0][0]
                    result['image_url'] = ""
            select_sql = "select id from foods where food_url='" + result['food_url'] + "'"
            update_sql = 'update foods set '       
            insert_sql = 'insert into foods('
            values = 'values('
            for key,value in result.iteritems(): 
                update_sql += key + "='" + str(value).replace("'","") + "', "                    
                insert_sql += key + ', '
                values += '%s ,'
            update_sql += "updated_at='"+date_str+"' where food_url='" + result['food_url'] +"'"
            insert_sql = insert_sql + 'created_at, updated_at) ' + values + "%s, %s)"
            #insert_sql = insert_sql[:-2] + ") " + values[:-2]+")"
            params = tuple(result.values())+(date_str,date_str)
            cls.util_db.execute_sql(select_sql)
            if cls.util_db.row_count() > 0:
                cls.util_db.execute_sql(update_sql)
            else:
                cls.util_db.execute_sql(insert_sql,params)
        
    @classmethod   
    def store_user_restaurants_by_id(cls,results): 
        date_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')         
        for result in results:  
            if 'score' in result.keys() and str(result["score"])=="":
                continue
            select_sql = "select id from user_restaurant_configs where user_id=" + str(result['user_id']) + " and restaurant_id=" + str(result['restaurant_id'])
            update_sql = 'update user_restaurant_configs set '       
            insert_sql = 'insert into user_restaurant_configs('
            values = 'values('
            for key,value in result.iteritems(): 
                update_sql += key + "='" + str(value).replace("'","") + "', "                    
                insert_sql += key + ', '
                values += '%s ,'
            update_sql += "updated_at='"+date_str+"' where user_id=" + str(result['user_id']) + " and restaurant_id=" + str(result['restaurant_id'])
            insert_sql = insert_sql + 'created_at, updated_at) ' + values + "%s, %s)"
            #insert_sql = insert_sql[:-2] + ") " + values[:-2]+")"
            params = tuple(result.values())+(date_str,date_str)
            cls.util_db.execute_sql(select_sql)
            if cls.util_db.row_count() > 0:
                cls.util_db.execute_sql(update_sql)
            else:
                cls.util_db.execute_sql(insert_sql,params)
        
    @classmethod
    def close_db_connection(cls):
        cls.util_db.close_connection()
        
    