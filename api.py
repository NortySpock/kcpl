from flask import Flask, jsonify, request
from kcpl import kcpl

app = Flask(__name__)

@app.route('/')
def main():
    return 'Hello, World!'
    
def @app.route('/api/evergy/getLastFewDays/<daysToLookback>')
    kcpl = KCPL()
    kcpl.login()

    # Get a list of daily readings
    # Note, there is more data available such as 'cost' and 'avgTemp'
    data = kcpl.getUsage()
    logging.info("Last usage reading: " + str(data[-1]))
    logging.info("Last usage reading: " + str(data[-1]["usage"]))

    # End your session by logging out
    kcpl.logout()
        