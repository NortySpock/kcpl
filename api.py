from flask import Flask, jsonify, request, abort, make_response
from kcpl import kcpl

fakedb = []
# import sqlite3
# conn = sqlite3.connect('example.db')

app = Flask(__name__)

@app.route('/')
def main():
    return 'Hello, World!'
    
@app.route('/api/evergy/getLastFewDays/<int:daysToLookBack>')
def getLastFewDaysFromEnergyCompany(daysToLookBack):
    kcpl = KCPL()
    kcpl.login()

    # Get a list of daily readings
    # Note, there is more data available such as 'cost' and 'avgTemp'
    data = kcpl.getUsage()
    logging.info("Last usage reading: " + str(data[-1]))
    logging.info("Last usage reading: " + str(data[-1]["usage"]))

    # End your session by logging out
    kcpl.logout()
   
@app.route('/api/local/insertOne/', methods=['POST'])  
@app.route('/api/local/insertOne', methods=['POST'])
def insertOne():
  if not request.json or not 'title' in request.json:
    abort(400)
  fakedb.append(request.json)
  return  make_response( jsonify({'success':True}),200 )
    

@app.route('/api/local/getLastFewDays/<int:daysToLookBack>')
def getLastFewDaysFromLocalDB(daysToLookBack):
  return [x for x in fakedb]
  
@app.route('/api/local/getAllFromDB/')  
def getAllFromLocalDB():
    return jsonify(fakedb)