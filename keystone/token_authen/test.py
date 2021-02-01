from keystoneauth1.identity import v3
from keystoneauth1.session import Session
from flask import Flask, request, jsonify
from novaclient import client
import gettoken

app = Flask(__name__)

OS_AUTH_URL = "http://172.19.242.10:5000/v3"

def create_session(token, project_name):
    auth = v3.Token(
        auth_url= OS_AUTH_URL,
        token=token,
        project_name=project_name,
        project_domain_name='Default'
    )
    return Session(auth=auth)

def nova_client(session, region):
    return client.Client("2", session=session, region_name=region)

@app.route('/')
def index():
    headers = request.headers
    token = headers.get('X-Auth-Token')
    project_name = headers.get('X-Tenant-Name')

    sess = gettoken.createSession(token, project_name)
    
    nova = nova_client(sess, 'HaNoi')
    list = nova.servers.list()
    token = sess.get_token()
    message = {
        "token": token,
        "list": str(list)
    }
    return jsonify(message=message), 200

if __name__ == '__main__':
    app.run(debug=True)