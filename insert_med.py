from lxml import etree
import pymysql
import os
host = os.environ['POEM_HOST']
user = os.environ['POEM_USER']
password = os.environ['POEM_PASS']
conn = pymysql.connect(host, user, password, 'poem')
cursor = conn.cursor()

def done(eid):
    cursor.execute('SELECT * FROM entry WHERE entry_id = %s', eid)
    entries = cursor.fetchall()
    if len(entries) > 0:
        entry = entries[0]
        cnt = 0
        for val in entry:
            if val == None:
                cnt += 1
        if cnt == 0:
            return True
    return False

def count_def(eid):
    cursor.execute('SELECT count(*) FROM definition WHERE entry_id = %s', eid)
    return cursor.fetchall()[0][0]

def del_def(eid):
    cursor.execute('DELETE FROM definition WHERE entry_id = %s', eid)
    
import os
files = os.listdir()
for file in files:
    if file.startswith('MED'):
        print(file)
        eid = file[:-5]
        try:
            with open(file, encoding='UTF-8') as file:
                r = file.read()
                tree = etree.HTML(r)
                if not done(eid):
                    print('Parsing %s.html entry' % eid)
                    word = tree.xpath('//div[@class="entry-headword"]//text()')[0].strip()
                    cursor.execute('SELECT id FROM word WHERE word = %s', word)
                    word_id = cursor.fetchall()
                    if len(word_id) == 0:
                        cursor.execute('INSERT INTO word(word) VALUES(%s)', word)
                        cursor.execute('SELECT id FROM word WHERE word = %s', word)
                        word_id = cursor.fetchall()
                    word_id = word_id[0][0]
                    propty = tree.xpath('//span[@class="entry-pos"]//text()')[0]
                    form = tree.xpath('//span[@class="FORM"]')[0]
                    form_raw_html = etree.tostring(form)
                    etymology = tree.xpath('//td[@class="etymology-list"]')[0]
                    etymology_row_html = etree.tostring(etymology)
                    cursor.execute('REPLACE INTO entry (entry_id, word, property, forms, etymology)VALUES(%s, %s, %s, %s, %s)', 
                                   (eid, word_id, propty, form_raw_html, etymology_row_html))
                print('Parsing %s.html definitions' % eid)
                definitions = tree.xpath('//div[@class="definition"]')
                if count_def(eid) < len(definitions):
                    del_def(eid)
                    for definition in definitions:
                        def_raw_html = etree.tostring(definition)
                        cursor.execute('INSERT INTO definition (entry_id, content) VALUES(%s, %s)', (eid, def_raw_html))
                conn.commit()
        except Exception as e:
            conn.rollback()
            print(e)
        
print('Disconnecting database...')
cursor.close()
conn.close()
