import hashlib
from datetime import datetime
import socket
import flask
from flask import request, jsonify

app = flask.Flask(__name__)

def get_current_IP(): 
    try: 
        host_name = socket.gethostname() 
        host_ip = socket.gethostbyname(host_name) 
        return host_ip
    except: 
        return "Unable to get Hostname and IP"

def hashDate(currentDate):

    hdate = hashlib.md5()
    hdate.update(str(currentDate).encode('utf-8'))    
    return str(hdate.hexdigest())

def msg_of_the_day():
    
    now = datetime.now()
    currentDate = now.strftime("%d/%m/%Y")
    currentTime = now.strftime("%H:%M:%S")
    currentIP = get_current_IP()
    currentDateHash = hashDate(currentDate)

    msg=[
        {'date' : currentDate,
        'time' : currentTime,
        'ip' : currentIP,
        'hash' : currentDateHash}
    ]

    return msg

@app.route('/', methods=['GET'])
def index():
    return 'Server Works!'
  
@app.route('/info', methods=['GET'])
def api_msg_of_the_day():
    return jsonify(msg_of_the_day())

if __name__ == '__main__':
    
    app.run(host='0.0.0.0')
