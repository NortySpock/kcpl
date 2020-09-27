from datetime import datetime, date,  timedelta
from flask import Flask, jsonify, request, abort, make_response
from kcpl import kcpl

import sqlite3

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
  try:
      con = sqlite3.connect("energy_usage.db")
      cur = con.cursor()
        
      
      sqlstatement = "INSERT INTO history (date, energy_use,peak_power_demand,peak_time,high_temp_F,low_temp_F,avg_temp_F)"
      
      
      cur.execute(sqlstatement)
      results = cur.fetchall()
      print("Results:"+str(results),flush=True)
      
  except sqlite3.Error as error:
    print("Failed to insert data into sqlite table", error)
  finally:
    if (con):
        con.close()
        print("The SQLite connection is closed")
  
  return  make_response( jsonify({'success':True}),200 )
    

@app.route('/api/local/getLastFewDays/<int:daysToLookBack>')
@app.route('/api/local/getLastFewDays/<int:daysToLookBack>/')
def getLastFewDaysFromLocalDB(daysToLookBack):
  
  print("daysToLookBack:"+str(daysToLookBack),flush=True)
  try:
      con = sqlite3.connect("energy_usage.db")
      cur = con.cursor()
      
      earliest_date = date.today() - timedelta(days=daysToLookBack)
      
      sqlstatement = "select date, energy_use,peak_power_demand,peak_time,high_temp_F,low_temp_F,avg_temp_F from history where active = 1 and date>='" +  str(earliest_date.isoformat())+"'"

      cur.execute(sqlstatement)
      results = cur.fetchall()
      print("Results:"+str(results),flush=True)
  
  except sqlite3.Error as error:
    print("Failed to get data from sqlite table", error)
  finally:
    if (con):
        con.close()
        print("The SQLite connection is closed")
  
  if len(results) == 0:
    return make_response('', 204)
  return jsonify(results)
  
@app.route('/api/local/getAllFromDB/')  
def getAllFromLocalDB():
  try:
    con = sqlite3.connect("energy_usage.db")
    cur = con.cursor()
    
    sqlstatement = "select rowid, date, energy_use,peak_power_demand,peak_time,high_temp_F,low_temp_F,avg_temp_F,active from history"
    
    cur.execute(sqlstatement)
    results = cur.fetchall()

  except sqlite3.Error as error:
    print("Failed to insert data into sqlite table", error)
  finally:
    if (con):
        con.close()
        print("The SQLite connection is closed")

  return jsonify(results)

@app.route('/api/local/cleanup')     
@app.route('/api/local/cleanup/')  
@app.route('/api/local/deactivateDupes/')
def cleanupDB():
  try:
    sqlstatement = ""
    with open('cleanup_script.sql') as f:
      sqlstatement = f.read()
        
    con = sqlite3.connect("energy_usage.db")
    cur = con.cursor()  
      
    cur.execute(sqlstatement)  

  except sqlite3.Error as error:
    print("Failed to cleanup sqlite table", error)
  finally:
    if (con):
        con.close()
        print("The SQLite connection is closed")
  return make_response('', 204)

@app.route('/api/local/test/')      
def test():
  my_date = date.today()
  print(my_date.isoformat())
  return my_date.isoformat()
  

