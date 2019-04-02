from flask import Flask, render_template, redirect, url_for
import pandas as pd
import json
from config import gkey
import pymongo

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.propertyDB

@app.route('/')
def welcome():
  return redirect(url_for('map'))

@app.route('/map')
def map():
  properties = db.locations.find({'DateRemoved': {'$not': ''}})
  return render_template('map.html', gkey=gkey, properties=getProperties())

@app.route('/property-list')
def propertyList():
  columns = ['ParcelID', 'Address', 'Ward', 'Neigh', 'AssN', 'Usage', 'Description', 'BldgSF', 'Front', 'Side1', 'LotSF', 'Latitude', 'Longitude', 'DateAdded', 'DateRemoved']
  return render_template('property-list.html', properties=getProperties(), columns=columns)

@app.route('/property/<propertyID>')
def propertyDetails(propertyID):
  propertyDetail = db.locations.find({'ParcelID': int(propertyID)})
  columns = ['ParcelID', 'Address', 'Ward', 'Neigh', 'AssN', 'Usage', 'Description', 'BldgSF', 'Front', 'Side1', 'LotSF', 'Latitude', 'Longitude', 'DateAdded', 'DateRemoved']
  # propertyDetail['Error'] = "Property not found"
  return render_template('property-detail.html', gkey=gkey, propertyDetail=propertyDetail, columns=columns)

def getProperties():
  return db.locations.find()

if __name__ == '__name__':
  app.run(debug=True, port=3000)