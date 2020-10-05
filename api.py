from datetime import datetime, date,  timedelta
from flask import Flask, jsonify, request, abort, make_response
from kcpl import kcpl
import json

import sqlite3

app = Flask(__name__)

@app.route('/')
def main():
    return 'Hello, World!'
    
@app.route('/api/evergy/getLastFewDays/<int:daysToLookBack>')
@app.route('/api/evergy/getLastFewDays/<int:daysToLookBack>/')
def getLastFewDaysFromEnergyCompanyAPI(daysToLookBack):
     
    data = getLastFewDaysFromEnergyCompany(daysToLookBack)
    print(jsonify(data))
    return jsonify(data)
    
    
@app.route('/api/evergy/getLastFewDaysAndStore/<int:daysToLookBack>')
@app.route('/api/evergy/getLastFewDaysAndStore/<int:daysToLookBack>/')   
def getLastFewDaysFromEnergyCompanyAPIAndStore(daysToLookBack):
    data = getLastFewDaysFromEnergyCompany(daysToLookBack)
    dbInsertList(data)
    return make_response( "",204 )

    
def getLastFewDaysFromEnergyCompany(daysToLookBack):
    earliest_date = date.today() - timedelta(days=daysToLookBack)
    
    creds = dict() 

    with open("credentials.json", 'r') as f:
        creds = json.loads(f.read())

    username = creds["username"]
    password = creds["password"]

    con = kcpl.KCPL(username, password)
    try:
        con.login()

        # Get a list of daily readings
        data = con.getUsage(earliest_date,date.today(),query_scale="d")        

    finally:
    # End your session by logging out
        con.logout()

    
    return data

    
@app.route('/api/evergy/getDateRangeAndStore')
@app.route('/api/evergy/getDateRangeAndStore/')   
def getDateRangeFromEnergyCompanyAPIAndStore():
    start_date = request.args.get("start")
    end_date = request.args.get("end")
    data = getDateRangeFromEnergyCompany(start_date,end_date)
    dbInsertList(data)
    return make_response( "",204 )

def getDateRangeFromEnergyCompany(start,end):
    if(start > end):
      #swap
      temp = end
      end = start 
      start = temp
    
    
    creds = dict() 

    with open("credentials.json", 'r') as f:
        creds = json.loads(f.read())

    username = creds["username"]
    password = creds["password"]

    con = kcpl.KCPL(username, password)
    try:
        con.login()

        # Get a list of daily readings
        data = con.getUsage(start,end,query_scale="d")

    finally:
    # End your session by logging out
        con.logout()

    return data
    
   
@app.route('/api/local/insertOne/', methods=['POST'])  
@app.route('/api/local/insertOne', methods=['POST'])
def insertOne():
  if not (request and request.is_json):
    abort(400)
  try:
      con = sqlite3.connect("energy_usage.db")
      cur = con.cursor()
        
        # {
        # "avgDemand": 0.0,
        # "avgTemp": 68.716667,
        # "billDate": "2020-09-24T00:00:00",
        # "billEnd": "0001-01-01T00:00:00",
        # "billStart": "0001-01-01T00:00:00",
        # "cost": 31.2612,
        # "date": "9/24/2020",
        # "demand": 3.156,
        # "isPartial": false,
        # "maxTemp": 79.9,
        # "minTemp": 57.2,
        # "peakDateTime": "8:45 p.m.",
        # "peakDemand": 3.156,
        # "period": "Thursday",
        # "usage": 28.1052
        # }
      print(str(request.json),flush=True)
        
      
      
      sqlstatement = "INSERT INTO history (date_of_use, energy_use,peak_power_demand,peak_time,high_temp_F,low_temp_F,avg_temp_F) VALUES(?,?,?,?,?,?,?)"
      
      
      cur.execute(sqlstatement, (
            request.json["billDate"][:10],
            request.json["usage"],
            request.json["peakDemand"],
            request.json["peakDateTime"],
            request.json["maxTemp"],
            request.json["minTemp"],
            request.json["avgTemp"]
            )
        )
      con.commit()
  except sqlite3.error as error:
    print("failed to insert data into sqlite table", error, flush=True)
  except sqlite3.warning as warning:
    print("warning on insert data into sqlite table", error, flush=True)
  finally:
    if (con):
        con.close()
        print("the sqlite connection is closed")
  
  return  make_response( "",204 )
    
@app.route('/api/local/insertList/', methods=['POST'])  
@app.route('/api/local/insertList', methods=['POST'])
def insertList():
  if not (request and request.is_json):
    abort(400)
    
  dbInsertList(request.json)
  
  
  return  make_response( "",204 )

def dbInsertList(list):
  try:
      print(str(list),flush=True)
      if len(list) == 0:
        return "No data was requested to be inserted";
        
      con = sqlite3.connect("energy_usage.db")
      cur = con.cursor()
        
      newTuples = []
      
      for thing in list:
        tup = (
            thing["billDate"][:10],
            thing["usage"],
            thing["peakDemand"],
            thing["peakDateTime"],
            thing["maxTemp"],
            thing["minTemp"],
            thing["avgTemp"]
            )
        newTuples.append(tup)
      
      sqlstatement = "INSERT INTO history (date_of_use, energy_use,peak_power_demand,peak_time,high_temp_F,low_temp_F,avg_temp_F) VALUES(?,?,?,?,?,?,?)"
      
      
      cur.executemany(sqlstatement, newTuples)
      con.commit()
  except sqlite3.error as error:
    print("failed to insert data into sqlite table", error, flush=True)
  except sqlite3.warning as warning:
    print("warning on insert data into sqlite table", error, flush=True)
  finally:
    if (con):
        con.close()
        print("the sqlite connection is closed")

@app.route('/api/local/getLastFewDays/<int:daysToLookBack>')
@app.route('/api/local/getLastFewDays/<int:daysToLookBack>/')
def getLastFewDaysFromLocalDB(daysToLookBack):
  
  print("daysToLookBack:"+str(daysToLookBack),flush=True)
  try:
      con = sqlite3.connect("energy_usage.db")
      cur = con.cursor()
      
      earliest_date = date.today() - timedelta(days=daysToLookBack)
      
      sqlstatement = "select date_of_use, energy_use,peak_power_demand,peak_time,high_temp_F,low_temp_F,avg_temp_F from history where active = 1 and date_of_use>='" +  str(earliest_date.isoformat())+"'"

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
  
@app.route('/api/local/getAllFromDB')
@app.route('/api/local/getAllFromDB/')
def getAllFromLocalDB():
  try:
    con = sqlite3.connect("energy_usage.db")
    cur = con.cursor()
    
    sqlstatement = "select rowid, date_of_use, energy_use,peak_power_demand,peak_time,high_temp_F,low_temp_F,avg_temp_F,active from history"
    
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
    print("Failed to cleanup sqlite table", error, flush=True )
  finally:
    if (con):
        con.close()
        print("The SQLite connection is closed")
  return make_response('', 204)

@app.route('/api/local/importLocalCSV/')      
def importLocalCSV():
  my_date = date.today()
  print(my_date.isoformat())
  return my_date.isoformat()
  

@app.route('/api/local/test/')      
def test():
  my_date = date.today()
  print(my_date.isoformat())
  return my_date.isoformat()
  

if __name__ == "__main__": 
    app.run(host ='0.0.0.0', port = 5000, debug = True) 
