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

OS_AUTH_URL = "https://hn-1.vccloud.vn:5000/v3"
OCTAVIA_AUTH_URL = "https://hn-1.vccloud.vn:9876"
region = "HaNoi"

keystone_session = get_token.createSession
nova_client = nova_cli.novaClient
octavia_client = octavia_cli.octaviCli(OCTAVIA_AUTH_URL, region)
query = config.query
querylbs = config.queryLbs

@app.route('/list/server/', endpoint='servers')
@app.route('/list/load-balancer/', endpoint='load-balancer')
def list():
    if request.endpoint == "servers":
        list_server = []
        # Lấy thông tin xác thực từ request header
        headers = request.headers
        token = headers.get('X-Auth-Token')
        project_name = headers.get('X-Tenant-Name')

        # Tạo session với token đã lấy được
        sess = keystone_session.create_session(OS_AUTH_URL, token, project_name)

        #Dùng session ở trên để lấy thông tin servers
        list_server = nova_client.list_server(sess, region)

        # Trả về kết quả
        message = {
            "List ID": str(list_server)
        }
        return jsonify(message=message), 200

    if request.endpoint == "load-balancer":
        # Lấy thông tin xác thực từ request header
        headers = request.headers
        token = headers.get('X-Auth-Token')
        project_name = headers.get('X-Tenant-Name')

        # Tạo session với token đã lấy được
        sess = keystone_session.create_session(OS_AUTH_URL, token, project_name)

        # List ID các thành phần của load balancer
        list_lbs = octavia_client.list_lbs(sess)

        # Trả về kết quả
        message = {
            "list": str(list_lbs)
        }
        return jsonify(message=message), 200

    else:
        return jsonify(message=None), 404

@app.route('/metric/server/', endpoint='server')
@app.route('/metric/load-balancer/', endpoint='loadblc')
def metric():
    if request.endpoint == "server":
            # Lấy thông tin xác thực từ request header
            headers = request.headers
            token = headers.get('X-Auth-Token')
            project_name = headers.get('X-Tenant-Name')

            # Tạo session với token đã lấy được
            sess = keystone_session.create_session(OS_AUTH_URL, token, project_name)
            
            # Lấy thông tin từ parameter
            sid = request.args.get('sid')
            name = request.args.get('name')
            value_type = request.args.get('value_type')
            metric = request.args.get('metric_type')

            list_servers = nova_client.list_server(sess, 'HaNoi')
            
            # Kiểm tra sid có trong list_servers ID?
            if sid in list_servers:
                query_dict = {
                    "cpu": query.query_cpu, "memory": query.query_ram, "disk": query.query_disk_size, \
                    "block": query.query_block_rw_iops, "netbytes": query.query_net_tx_rx_bytes, \
                    "netpkt": query.query_net_tx_rx_pkt, "prometheus": query.query_prometheus
                            }

                # query thông tin metric
                if metric in query_dict:
                    queries = query_dict.get(str(metric))
                else:
                    return jsonify(message=None), 404
                response = sess.get(queries(sid, name, value_type))
            
                # Trả về kết quả
                data = response.json()
                return jsonify(message=data), 200
            else:
                message = {
                    "Message": "Bad Parameter. Wrong Server ID input!"
                }
                return jsonify(message=message), 400
    
    if request.endpoint == "loadblc":
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
            pool = request.args.get('backend')
            metric = request.args.get('metrictype')
            # name = request.args.get('name')
            time = request.args.get('time')
            time_interval = request.args.get('time_interval')

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
                if metric in query_dict:
                    queries = query_dict.get(str(metric))
                else:
                    return jsonify(message=None)
                response = sess.get(queries(lbid, listeners, backend_id, time, time_interval="30s"))
                data = response.json()
                return jsonify(message=data), 200
            else:
                message = {
                    "Message": "Bad Parameter. Wrong ID input!"
                }
                return jsonify(message=message), 400
    else:
        return jsonify(message=None), 404

if __name__ == '__main__':
    app.run(debug=True)