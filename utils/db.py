import pymysql
from dbutils.pooled_db import PooledDB
from pymysql import cursors
Pool = PooledDB(
    creator=pymysql,#使用链接数据库的模块
    maxconnections=10,#连接池允许的最大连接数，0和none表示不限制
    mincached=2,#初始化时，至少创建的空闲的链接，0表示不创建
    maxcached=3,#连接池中最多闲置的链接，0和none不限制
    blocking=True, #连接池没有可用连接后，是否阻塞等待。true,等待；false，不等待然后报错
    setsession=[], # 开始会话前执行的命令列表。如【set datestyle to, set time zone】
    ping=0,
    host='127.0.0.1', port=3306, user='root', passwd='zhangxiao', charset='utf8', db='day21'
)

def fetch_one(sql, params):
    conn = Pool.connection()
    cursor = conn.cursor(cursor=cursors.DictCursor)
    cursor.execute(sql, params)
    #cursor.execute("select * from user where token=%s", [token, ])
    result = cursor.fetchone()
    cursor.close()
    conn.close()#不是关闭连接，而是将死连接交还给连接池
    return result

def fetch_all(sql, params):
    conn = Pool.connection()
    cursor = conn.cursor(cursor=cursors.DictCursor)
    cursor.execute(sql, params)
    #cursor.execute("select * from user where token=%s", [token, ])
    # 取所有数据
    result = cursor.fetchall()
    cursor.close()
    conn.close()#不是关闭连接，而是将死连接交还给连接池
    return result

def insert(sql, params):
    conn = Pool.connection()
    cursor = conn.cursor(cursor=cursors.DictCursor)
    cursor.execute(sql, params)
    #cursor.execute("select * from user where token=%s", [token, ])
    # 取所有数据
    conn.commit()
    cursor.close()
    conn.close()#不是关闭连接，而是将死连接交还给连接池
    return cursor.lastrowid
