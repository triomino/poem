from lxml import etree
import pymysql
import re
import requests
import random
import time
import os

host = os.environ['POEM_HOST']
user = os.environ['POEM_USER']
password = os.environ['POEM_PASS']
db = pymysql.connect(host, user, password, 'poem')
cursor = db.cursor()

host = 'https://quod.lib.umich.edu'

cursor.execute('SELECT word FROM word')
words = cursor.fetchall()
words = list(map(lambda x: x[0], words))

def invalid(fname):
    with open(fname) as f:
        c = f.read()
        if c.find('Service Unavailable') != -1:
            return True
    return False


for word in words:
    if len(word) > 0:
        try:
            filename = 'html/word_%s.html' % word
            if not os.path.exists(filename):
                continue
            with open(filename, 'r') as f:
                content = f.read()
                tree = etree.HTML(content)
                elements = tree.xpath('//a[@data-context-href]')
                print(word)
                for e in elements:
                    link = e.attrib['data-context-href']
                    # print(link)
                    med = re.findall('(MED(\d*\.\d+|\d+))', link)
                    if len(med) > 0:
                        url = host + link
                        fname = 'html/%s.html' % med[0][0]
                        if not os.path.exists(fname) or invalid(fname):
                            response = requests.get(url)
                            print('GET', url, response.status_code)
                            cont = response.content
                            with open(fname, 'wb+') as g:
                                g.write(cont)
                            time.sleep(random.randint(2, 8))
        except Exception as e:
            # do nothing
            print(e)

