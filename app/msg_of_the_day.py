import hashlib
from datetime import datetime
import socket
import flask
from flask import request, jsonify, Response
import prometheus_client
from prometheus_client import Counter, Histogram
import time
import sys

REQUEST_COUNT = Counter(
    'request_count', 'App Request Count',
    ['app_name', 'method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency',
    ['app_name', 'endpoint']
)

def start_timer():
    request.start_time = time.time()

def stop_timer(response):
    resp_time = time.time() - request.start_time
    REQUEST_LATENCY.labels('Message of the day', request.path).observe(resp_time)
    return response

def record_request_data(response):
    REQUEST_COUNT.labels('Message of the day', request.method, request.path,
            response.status_code).inc()
    return response

def setup_metrics(app):
    app.before_request(start_timer)
    app.after_request(record_request_data)
    app.after_request(stop_timer)

app = flask.Flask(__name__)
setup_metrics(app)

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
    return {'message': 'Server Works!'}
  
@app.route('/info', methods=['GET'])
def api_msg_of_the_day():
    return jsonify(msg_of_the_day())

@app.route('/metrics')
def metrics():
    return Response(prometheus_client.generate_latest(), mimetype=str('text/plain; version=0.0.4; charset=utf-8'))

if __name__ == '__main__':
    
    app.run(host='0.0.0.0')
