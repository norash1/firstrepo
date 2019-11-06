#optional ideas:
#   - force any email property to be lowercase
#   - add flexibility with location of identity column
#   - add another prompt to continue with network requests after reviewing json dump

import json
import csv
import sys
import requests
### first ask for app id and the raw csv file
app_id = raw_input("specify app id: ")
raw_csv = raw_input("specify csv file (include '.csv'): ")
### open file and extract the headers. FIRST COLUMN MUST BE IDENTITY
file = open(raw_csv)
csv_reader = csv.reader(file)
property_list = next(csv_reader)[1:]
### create users list and build nested objects
users = []
for row in csv_reader:
    identity = row[0]
    properties = {} ### must nest properties
    i=1 ### to traverse through row
    for property in property_list:
        properties[property] = row[i]
        i+=1
    user = {"identity":identity, "properties":properties}
    users.append(user)

### OPTIONAL: open json file and dump formatted stuff to it
jsonfile = open(raw_csv[:-3]+"json", 'w')
raw_json = {"app_id": app_id, "users": users}
json.dump(raw_json, jsonfile)

# following Kevin's script here
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

headers = {'Content-type': 'application/json'}
url = 'https://heapanalytics.com/api/add_user_properties'

batches = list(chunks(users, 500))
for batch in batches:
    data = {'app_id':app_id,'users':batch}
    r = requests.post(url, json = data, headers=headers)
    print("POST response is: " + r.text)
