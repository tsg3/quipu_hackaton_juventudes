import pymysql
import os

def db_connect():
    path = os.path.dirname(__file__)
    path = os.path.abspath(os.path.join(path, "db_config"))
    file = open(path, "r")
    connection = pymysql.connect(host='localhost',
        user='quipu',
        password=file.read(),
        db='quipu_db')
    file.close()
    return connection