import requests
import time
import random
import pymysql
import os

host = os.environ['POEM_HOST']
user = os.environ['POEM_USER']
password = os.environ['POEM_PASS']
db = pymysql.connect(host, user, password, 'poem')
cursor = db.cursor()

url = 'https://quod.lib.umich.edu/m/middle-english-dictionary/dictionary?utf8=%E2%9C%93&search_field=hnf&q='
cursor.execute('SELECT word FROM word')
words = cursor.fetchall()
words = list(map(lambda x: x[0], words))
downloaded = os.listdir()
for word in words:
    if len(word) > 0:
        filename = 'word_%s.html' % word
        if filename in downloaded:
            continue
        r = requests.get(url + word)
        print('GET', url + word, r.status_code)
        if r.status_code == requests.codes.ok:
            with open(filename, 'wb+') as file:
                file.write(r.content)
        time.sleep(random.randint(5, 10))

cursor.close()
db.close()
