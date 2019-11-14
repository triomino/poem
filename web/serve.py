import http.server
from urllib.parse import urlparse
import json
import os
from db import run_sql

PORT = 8080

def do_nothing():
    return 0

class Handler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        path = self.path
        if path.startswith('/confessio'):
            query = urlparse(path).query
            q = dict(qc.split("=") for qc in query.split("&"))
            sql = ' '.join(['SELECT row, `column`, word.word, count(*), confessio.entry, word.id',
                    'FROM confessio LEFT JOIN word ON confessio.word = word.id',
                        'LEFT JOIN entry ON confessio.word = entry.word',
                    'WHERE confessio.section = %s  GROUP BY row, `column`'])
            response = run_sql(sql, q['section'])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        elif path.startswith('/entry'):
            query = urlparse(path).query
            q = dict(qc.split("=") for qc in query.split("&"))
            sql = ' '.join(['SELECT id, property, forms, etymology, content, word',
                            'FROM entry LEFT JOIN definition ON entry.id = definition.eid',
                            'WHERE word = %s'])
            response = run_sql(sql, q['word'])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            super().do_GET()

with http.server.HTTPServer(("0.0.0.0", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()


