import couchdb
import json
from analyzer import summary

VmIPs = list()
CouchDB = list()
Database = list()
backDatabase = list()

f = open('VmList', 'r')
for line in f:
    line = line.replace('\n', '')
    VmIPs.append(line)

for IPs in VmIPs:
    couchServer = couchdb.Server(IPs)
    CouchDB.append(couchServer)

totalCouchServer = len(CouchDB)

for index in range(totalCouchServer):
     try:
        db = CouchDB[index]['twitter_big_data']
        bdb = CouchDB[(index+1)%totalCouchServer]['backup_twitter_big_data']
     except:
    	db = CouchDB[index].create('twitter_big_data')
        bdb = CouchDB[(index+1)%totalCouchServer].create('backup_twitter_big_data')
     Database.append(db)
     backDatabase.append(bdb) 
    

f = open('Crawling_Output', 'r')
count = 0
for line in f:
	if len(line)>1:
		try:
			doc = json.loads(line)
			doc['_id'] = str(doc['id'])
			doc['result'] = summary(doc)
			dbID = abs(hash(doc['_id']))%totalCouchServer
			Database[dbID].save(doc)
			backDatabase[dbID].save(doc)
			count=count+1
		except (ValueError,couchdb.http.ResourceConflict) as e:
			pass
print count
