from lxml import etree
import pymysql

import os
host = os.environ['POEM_HOST']
user = os.environ['POEM_USER']
password = os.environ['POEM_PASS']
db = pymysql.connect(host, user, password, "poem")
cursor = db.cursor()
try:
    with open('confessio.html', 'r', encoding='UTF-8') as file:
        content = file.read()
        tree = etree.HTML(content)
        lines = tree.xpath('//div[@class="line"]')
        for line in lines:
            [section, row] = line.attrib['n'].split('.')
            row = int(row)
            values = []
            for column, word in enumerate(line.text.split()):
                word = word.lower()
                word = ''.join(x for x in word if x.isalpha())
                cursor.execute('SELECT id FROM word WHERE word = %s', word)
                result = cursor.fetchall()
                if len(result) > 0:
                    number = result[0][0]
                else:
                    cursor.execute('INSERT INTO word (word) VALUES(%s)', word)
                    cursor.execute('SELECT id FROM word WHERE word = %s', word)
                    result = cursor.fetchall()
                    number = result[0][0]
                values.extend((row, column, number, section))
            n = len(values) // 4
            cursor.execute('REPLACE INTO `confessio`(`row`, `column`, `word`, `section`)VALUES' + (','.join(['(%s, %s, %s, %s)' for it in range(n)])), values)
            db.commit()
            print('line %d ok' % row)
except KeyboardInterrupt:
    print('KeyboardInterrupt received. Stopping...')
print('Disconnecting database...')
cursor.close()
db.close()