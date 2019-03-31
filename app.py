from flask import Flask, render_template
import pandas as pd
from config import gkey

app = Flask(__name__)

@app.route('/')
def welcome():
  return render_template('index.html', gkey=gkey, coordinates=coordinates)

def getCoordinates():
  properties = pd.read_csv("data/properties.csv")
  coordinates = []
  for index, row in properties.iterrows():
      coordinates.append(tuple((row["Latitude"], row["Longitude"])))
  return coordinates

coordinates = getCoordinates()

if __name__ == '__name__':
  app.run(debug=True, port=3000)