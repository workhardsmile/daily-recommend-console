# encoding=utf8 
import os,sys

#os.getcwd()
#os.path.pardir
library_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"library"))
for parent,dirnames,filenames in os.walk(library_path):
    for dirname in dirnames:
        dir_path = os.path.join(parent,dirname)
        if not dir_path in sys.path:
            sys.path.append(dir_path)
           
    for filename in filenames:
        if filename.strip().endswith(".py"):
            temp = filename.strip().replace(".py","",1)
            if not temp in sys.modules:
                temp = __import__(temp)
            else:
                eval("import "+ temp)
                temp = eval("reload("+temp+")")
reload(sys)
sys.setdefaultencoding('utf8')