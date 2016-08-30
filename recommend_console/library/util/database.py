import MySQLdb
from recommend_console import settings

class UtilDatabase(object):
    __host = None
    __databse = None
    __user = None
    __password =  None
    __charset = None
    __port = None
    __conn = None
    __cursor = None

    def __init__(self,db_host=None,db_name=None,db_user=None,db_passwd=None,db_charset=None,db_port=None):
        if self.__host==None:
            self.__host = settings.DB_HOST
        else:
            self.__host = db_host
            
        if self.__databse==None:
            self.__databse = settings.DB_NAME
        else:
            self.__databse = db_name
            
        if self.__user==None:
            self.__user = settings.DB_USER
        else:
            self.__user = db_user
            
        if self.__password==None:
             self.__password = settings.DB_PASSWORD
        else:
             self.__password = db_passwd
             
        if db_charset==None:
            self.__charset = settings.DB_CHARSET
        else:
            self.__charset = db_charset
            
        if db_port==None:
            self.__port = settings.DB_PORT
        else:
            self.__port = db_port
      
    def open_connection(self):
        try:
            if self.__conn==None:
                self.__conn = MySQLdb.connect(host=self.__host,user=self.__user,passwd=self.__password,db=self.__databse,charset=self.__charset,port=self.__port)  
            if self.__cursor==None:
                self.__cursor = self.__conn.cursor()
        except MySQLdb.Error,e:
            print "Mysql Connection Error %d: %s" % (e.args[0],e.args[1])
        
    def execute_sql(self,sql_str,params=None):
        self.open_connection()
        n = None
        try:
            if params==None or params==():
                n = self.__cursor.execute(sql_str)
            else:
                n = self.__cursor.execute(sql_str,tuple(params))
            if self.__conn:
                self.__conn.commit()
        except MySQLdb.Error,e:
            print "Mysql Execution Error %d: %s \n%s \n%s" % (e.args[0],e.args[1],sql_str,params)
        return n
    
    def commit(self):
         if self.__conn:
            self.__conn.commit()
        
    def close_connection(self):
        try:
            if self.__cursor:           
                self.__cursor.close() 
            if self.__conn:
                self.__conn.commit()
                self.__conn.close()
        except MySQLdb.Error,e:
            print "Mysql Close Error %d: %s" % (e.args[0],e.args[1])
            
    def execute(self,sql_str,params=None):
        self.execute_sql(sql_str, params)
        self.close_connection()
        
    def row_count(self):
        n = 0
        if self.__cursor:
            n = int(self.__cursor.rowcount)
        return n
    
    def get_rows(self):
        rows = []
        if self.__cursor:
            rows = self.__cursor.fetchall()
        return rows