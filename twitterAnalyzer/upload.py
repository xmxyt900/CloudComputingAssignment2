import json
import os
f = open('filenames', 'r')
for line in f:
    line = line.replace('\n', '')
    command = "curl -X GET http://localhost:5984/documents/all_json"
    res = os.popen(command).read()
    doc = json.loads(res)	
    rev = doc['_rev']
    command = "curl -X PUT -d @"+line+" http://localhost:5984//documents/all_json/"+line+"?rev="+rev
    res = os.popen(command).read()
