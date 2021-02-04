from keystoneauth1.identity import v3
from keystoneauth1.session import Session
from flask import Flask, request, jsonify
import requests
import gettoken
import novaCli

app = Flask(__name__)

OS_AUTH_URL = "https://hn-1.vccloud.vn:5000/v3"
list_server = []

keystone_session = gettoken.createSession
nova_client = novaCli.novaClient

@app.route('/')
def index():
    headers = request.headers
    token = headers.get('X-Auth-Token')
    project_name = headers.get('X-Tenant-Name')

    sess = keystone_session.create_session(OS_AUTH_URL, token, project_name)

    nova = nova_client.nova(sess, 'HaNoi')
    
    for info in nova.servers.list():
        # list_server.append(info.name)
        # list_server.append(info.addresses)
        # list_server.append(info.status)
        list_server.append(info.id)
    
    token = sess.get_token()
    message = {
        "token": token,
        "list": str(list_server),
    }
    return jsonify(message=message), 200

@app.route('/metric')
def GET():
    headers = request.headers
    sid = headers.get('X-Server-ID')
    response = requests.get(f'https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/4/query?db=publicthor&q=SELECT mean(\"value\") FROM \"instances\" WHERE (\"tags1\" =~ /^{sid}$/ AND \"tags2\" = \'libvirt-kvm\' AND \"tags3\" = \'cpu\' AND \"tags4\" = \'total\' AND \"tags5\" = \'time\') AND time >= now() - 24h GROUP BY time(2m) fill(none)&epoch=ms')
    data = response.json()
    return jsonify(message=data), 200

if __name__ == '__main__':
    app.run(debug=True)