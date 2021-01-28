from flask import Flask, request, jsonify
from prometheus_client import start_http_server, Counter
app = Flask(__name__)

REQUEST_COUNT = Counter('request_count', 'descrition', ["app_type", 'endpoint'])

@app.route('/')
def index(self):
    REQUEST_COUNT.labels('from flask', self.path).inc
    headers = request.headers
    auth = headers.get("X-Username")
    if auth == 'hoanganh':
        message = {
            "Status": "OK",
            "Your Token is": "123asdf"
        }
        return jsonify(message), 200
    else:
        return jsonify({"message": "ERROR: Unauthorized"}), 401

if __name__ == '__main__':
    app.run()
    start_http_server(8005)