import json
import os
import couchdb

couchServer = couchdb.Server()
viewArray = ['drink_true', 'negativegearing_true', 'political_true']
mapFunctions = ['\"map\":\"function(doc){if(doc.result.analysis.drink){var obj = new Object();obj.text = doc.text;obj.created_at  = doc.created_at;obj.place = doc.place;obj.coordinates = doc.coordinates;obj.sentiment = doc.result.sentiment;var jsonString= JSON.stringify(obj);var arr = JSON.parse(jsonString);emit(doc.id, arr);}}\"','\"map\":\"function(doc){if(doc.result.analysis.negativegearing){var obj = new Object();obj.text = doc.text;obj.created_at  = doc.created_at;obj.place = doc.place;obj.coordinates = doc.coordinates;obj.sentiment = doc.result.sentiment;var jsonString = JSON.stringify(obj);var arr = JSON.parse(jsonString);  emit(doc.id, arr);}}\"','\"map\":\"function(doc){if(doc.result.analysis && (!doc.result.analysis.negativegearing || !doc.result.analysis.drink)){var obj = new Object();obj.text = doc.text;obj.created_at  = doc.created_at;obj.place = doc.place;obj.coordinates = doc.coordinates;obj.sentiment = doc.result.sentiment;var jsonString= JSON.stringify(obj);var arr = JSON.parse(jsonString);emit(doc.id, arr);}}\"']

for index in range(len(viewArray)):
    try:
        del couchServer[viewArray[index]]
        db = couchServer.create(viewArray[index])
    except:
        db = couchServer.create(viewArray[index])

VmIPs = list()
f = open('NectarIP', 'r')
for line in f:
    line = line.replace('\n', '')
    VmIPs.append(line)

for index in range(len(viewArray)):
    for IPs in VmIPs:
        command2 = "curl -X POST http://"+IPs+":5984/twitter_data/_temp_view -d '{"+mapFunctions[index]+"}' -H \"Content-type: application/json\">tempView.json"
        res2 = os.popen(command2).read()
        with open('tempView.json') as data_file:    
    	    data = json.load(data_file)
        modifiedData = {}
        modifiedData['docs'] = data['rows']
        with open('rawdata.json', 'w') as outfile:
    	    json.dump(modifiedData, outfile)
        command3 = "curl -d @rawdata.json -H \"Content-type: application/json\" -X POST http://127.0.0.1:5984/"+viewArray[index]+"/_bulk_docs"
        res3 = os.popen(command3).read()


