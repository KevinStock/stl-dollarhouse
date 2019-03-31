from flask import Flask, render_template
import pandas as pd
from config import gkey

app = Flask(__name__)

@app.route('/')
def welcome():
  return render_template('index.html', gkey=gkey, properties=properties)

def getProperties():
  data = pd.read_csv("data/properties.csv")
  properties = data.to_dict('records')
  return properties

properties = getProperties()

if __name__ == '__name__':
  app.run(debug=True, port=3000)