from flask.globals import session
from keystoneauth1.identity import V3ApplicationCredential, v3
from keystoneauth1.session import Session
from flask import Flask, request, jsonify
import requests
import get_token
import nova_cli
import octavia_cli
import config

app = Flask(__name__)

OS_AUTH_URL = "https://url:5000/v3"
list_server = []

keystone_session = get_token.createSession
nova_client = nova_cli.novaClient
octavia_client = octavia_cli.octaviCli("https://url:9876", "HaNoi")
query = config.query
querylbs = config.queryLbs

@app.route('/')
def index():
    # Lấy thông tin xác thực từ request header
    headers = request.headers
    token = headers.get('X-Auth-Token')
    project_name = headers.get('X-Tenant-Name')

    # Tạo session với token đã lấy được
    sess = keystone_session.create_session(OS_AUTH_URL, token, project_name)

    #Dùng session ở trên để lấy thông tin servers
    # nova = nova_client.nova(sess, 'HaNoi')
    
    # for info in nova.servers.list():
    #     # list_server.append(info.name)
    #     # list_server.append(info.addresses)
    #     # list_server.append(info.status)
    #     list_server.append(info.id)
    list_ser = octavia_client.list_lbs(sess)

    
    # Trả về kết quả
    message = {
        "list": str(list_ser)
    }
    return jsonify(message=message), 200

@app.route('/metric')
def GET():
    # Lấy thông tin xác thực từ request header
    headers = request.headers
    token = headers.get('X-Auth-Token')
    project_name = headers.get('X-Tenant-Name')

    # Tạo session với token đã lấy được
    sess = keystone_session.create_session(OS_AUTH_URL, token, project_name)
    
    # Lấy thông tin từ parameter
    sid = request.args.get('sid')
    name = request.args.get('name')
    type = request.args.get('type')
    metric = request.args.get('metrictype')

    list_servers = nova_client.list_server(sess, 'HaNoi')
    
    # Kiểm tra sid có trong list_servers ID?
    if sid in list_servers:
        query_dict = {"cpu": query.query_cpu, "memory": query.query_ram, "disk": query.query_disk_size, \
                      "block": query.query_block_rw_iops, "netbytes": query.query_net_tx_rx_bytes, \
                      "netpkt": query.query_net_tx_rx_pkt, "prometheus": query.query_prometheus}

        # query thông tin metric
        queries = query_dict.get(str(metric))
        response = sess.get(queries(sid, name, type))
    
        # Trả về kết quả
        data = response.json()
        return jsonify(message=data), 200
    else:
        message = {
            "Message": "Bad Parameter. Wrong Server ID input!"
        }
        return jsonify(message=message), 400

@app.route('/lbmetric')
def get_lbmetric():
    # Lấy thông tin xác thực từ request header
    headers = request.headers
    token = headers.get('X-Auth-Token')
    project_name = headers.get('X-Tenant-Name')

    # Tạo session với token đã lấy được
    sess = keystone_session.create_session(OS_AUTH_URL, token, project_name)
    dict_lbs = octavia_client.list_lbs(sess)
    
    # Lấy thông tin từ parameter
    lbid = request.args.get('lbid')
    listeners = request.args.get('frontend')
    pool = request.args.get('Backend')
    metric = request.args.get('metrictype')
    name = request.args.get('name')
    time = request.args.get('time')

    backend_id = pool+"_"+listeners

    if True:
        query_dict = {
            "req_per_sec_front": querylbs.req_per_sec_frontend, "stt_code_front_2xx": querylbs.status_code_frontend_2xx,
            "stt_code_front_3xx": querylbs.status_code_frontend_3xx, "stt_code_front_4xx": querylbs.status_code_frontend_4xx,
            "stt_code_front_5xx": querylbs.status_code_frontend_5xx, "data_transf_front_in": querylbs.data_transfer_frontend_in,
            "data_transf_front_out": querylbs.data_transfer_frontend_out, "req_per_sec_back": querylbs.req_per_sec_backend,
            "stt_code_back_2xx": querylbs.status_code_backend_2xx, "stt_code_back_3xx": querylbs.status_code_backend_3xx,
            "stt_code_back_4xx": querylbs.status_code_backend_4xx, "stt_code_back_5xx": querylbs.status_code_backend_5xx,
            "data_transf_back_in": querylbs.data_transfer_backend_in, "data_transf_back_out": querylbs.data_transfer_backend_out,
            "downtime_back": querylbs.downtime_backend, "queue_size_back": querylbs.queuesize_backend, "err_conn_per_sec_back": querylbs.error_connection_per_second_backend,
            "avg_back_resp_time": querylbs.average_backend_response_time, "err_resp_rate_back": querylbs.error_response_rate_backend, "rate_sess_per_sec_back": querylbs.rate_session_per_second_backend

            }
        queries = query_dict.get(str(metric))
        response = sess.get(queries(lbid, listeners, backend_id, time))
        data = response.json()
        return jsonify(message=data), 200
    else:
        message = {
            "Message": "Bad Parameter. Wrong ID input!"
        }
        return jsonify(message=message), 400

if __name__ == '__main__':
    app.run(debug=True)