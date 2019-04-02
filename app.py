from flask import Flask, render_template, redirect, url_for
import pandas as pd
import json
from config import gkey
import pymongo

app = Flask(__name__)

# mongodb connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.propertyDB

# root route which redirects to /map
@app.route('/')
def welcome():
  return redirect(url_for('map'))

# displays map with all available properties
@app.route('/map')
def map():
  properties = []
  for prop in db.locations.find({'DateRemoved': ''}):
    properties.append(prop)
  return render_template('map.html',
                         gkey=gkey,
                         properties=properties)

# displays table of all properties that have been made available since inception
@app.route('/property-list')
def propertyList():
  return render_template('property-list.html',
                         properties=getProperties(),
                         columns=getColumns())

# shows individual property details
@app.route('/property/<propertyID>')
def propertyDetails(propertyID):
  propertyDetail = list(db.locations.find({'ParcelID': int(propertyID)}))
  if (len(propertyDetail) == 0):
    propertyDetail = {'Error': 'Property Not Found'}
  return render_template('property-detail.html',
                         gkey=gkey,
                         propertyDetail=propertyDetail,
                         columns=getColumns())

# gets all properties from mongodb
def getProperties():
  return db.locations.find()

# returns columns for display on /property-list and /property-detail
def getColumns():
  return ['ParcelID', 'Address', 'Ward', 'Neigh', 'AssN', 'Usage', 'Description',
          'BldgSF', 'Front', 'Side1', 'LotSF', 'Latitude', 'Longitude', 'DateAdded', 'DateRemoved']

if __name__ == '__name__':
  app.run(debug=True, port=3000)