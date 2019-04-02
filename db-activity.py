import pandas as pd
import pymongo
import requests
from config import gkey

# connect to mongodb
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.propertyDB

# initial insert 3-1-2019
# def getProperties():
#   data = pd.read_csv("data/properties.csv")
#   properties = data.to_dict('records')
#   for prop in properties:
#     prop['DateAdded'] = '2019-03-01'
#     prop['DateRemoved'] = ''
#   return properties

# insert properties into mongodb
# db.locations.insert_many(getProperties())

# append DateAdded and DateRemoved to documents
# db.locations.update_many({}, {'$set': {'DateAdded': '2019-03-01'}})
# db.locations.update_many({}, {'$set': {'DateRemoved': ''}})

# 4-1-2019 update
def getProperties():
  data = pd.read_csv("data/4-1-19-DHPP-List.csv")
  properties = data.to_dict('records')
  for prop in properties:
    prop['DateAdded'] = '2019-04-01'
    prop['DateRemoved'] = ''
  return properties

# collect new properties
newProperties = []
for prop in getProperties():
  if isProperty(prop) == False:
    newProperties.append(prop)

# collect removed properties
removedProperties = []
for doc in db.locations.find():
  if removedProperty(doc) == True:
    removedProperties.append(doc)
      
# check if property in new list already exists
def isProperty(location):
  for doc in db.locations.find():
    if str(doc['ParcelID']) == str(location['ParcelID']):
      return True
  return False

# check if exisiting property has been removed
def removedProperty(location):
  for prop in getProperties():
    if str(prop['ParcelID']) == str(location['ParcelID']):
      return False
  return True

# get and set coordinates for new addresses
base_url = "https://maps.googleapis.com/maps/api/geocode/json?key=" + gkey + "&address="
for prop in newProperties:
  url = base_url + prop['Address'].replace(" ", "%20") + ",Saint%20Louis,MO"
  geo_data = requests.get(url).json()
  db.locations.update_one({'ParcelID': prop['ParcelID']}, {'$set': {'Latitude': geo_data["results"][0]["geometry"]["location"]["lat"]}})
  db.locations.update_one({'ParcelID': prop['ParcelID']}, {'$set': {'Longitude': geo_data["results"][0]["geometry"]["location"]["lng"]}})

# append DateRemoved to removed properties
for prop in removedProperties:
  db.locations.update({'ParcelID': prop['ParcelID']}, {'$set': {'DateRemoved': '2019-04-01'}})

# add new properties to mongodb
db.locations.insert_many(newProperties)
