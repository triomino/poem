from lxml import etree
import pymysql
import re
import os
host = os.environ['POEM_HOST']
user = os.environ['POEM_USER']
password = os.environ['POEM_PASS']
db = pymysql.connect(host, user, password, 'poem')
cursor = db.cursor()

files = os.listdir('html')
for file in files:
    if file.startswith('word_'):
        word = file[5:-5]
        try:
            with open('html/' + file, encoding='UTF-8') as file:
                r = file.read()
                tree = etree.HTML(r)
            
                print('Parsing word_%s.html' % word)
                nodes = tree.xpath('//a[@data-context-href]')
                for node in nodes:
                    med = re.findall('(MED(\d*\.\d+|\d+))', node.attrib['data-context-href'])
                    print(word, med[0][0])
                    cursor.execute('REPLACE INTO search_result (wid, eid) SELECT word.id, entry.id FROM word, entry WHERE word.word = %s AND entry.entry_id = %s', 
                                    (word, med[0][0]))
                db.commit()
        except Exception as e:
            db.rollback()
            print(e)
            raise(e)
        
print('Disconnecting database...')
cursor.close()
db.close()
