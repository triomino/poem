import pymysql
import os
host = os.environ['POEM_HOST']
user = os.environ['POEM_USER']
password = os.environ['POEM_PASS']

def run_sql(sql, p = None):
    db = pymysql.connect(host, user, password, 'poem')
    result = None
    with db.cursor() as cursor:
        print(sql % p)
        cursor.execute(sql, p)
        result = cursor.fetchall()
    db.close()
    return result

