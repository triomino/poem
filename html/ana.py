import os 
for fname in os.listdir():
    if fname.endswith('.html'):
        with open(fname) as f:
            c = f.read()
            if c.find('Service Unavailable') != -1:
                print(fname)