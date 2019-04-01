from flask import Flask, render_template, redirect, url_for
import pandas as pd
import json
from config import gkey

app = Flask(__name__)

@app.route('/')
def welcome():
  return redirect(url_for('map'))

@app.route('/map')
def map():
  return render_template('map.html', gkey=gkey, properties=properties)

@app.route('/property-list')
def propertyList():
  return render_template('property-list.html', properties=properties)

@app.route('/property/<propertyID>')
def propertyDetail(propertyID):
  propertyDetail = {}
  for prop in properties:
    if prop['ParcelID'] == int(propertyID):
      propertyDetail = prop
      break
    else:
      propertyDetail['Error'] = "Property not found"
  return render_template('property-detail.html', gkey=gkey, propertyDetail=propertyDetail)

def getProperties():
  data = pd.read_csv("data/properties.csv")
  properties = data.to_dict('records')
  return properties

properties = getProperties()
removed = [43903002700,52610004500,45030500200,48720002400,11680002100,44780004900,44780005200,44780005400,44780005800,44780006500,44780007000,36610001200,35580000100,44160500800,50380001600,45140000800,45140001100,45140002000,45140002100,45320003600,51990004900,53430003000,53460003800,53600004300,57860000200,54830002700,56720103000,53220002500,53940002000,55310002400,55560001300]
for prop in properties:
  if prop['ParcelID'] in removed:
    prop['Removed'] = True
  else:
    prop['Removed'] = False



if __name__ == '__name__':
  app.run(debug=True, port=3000)