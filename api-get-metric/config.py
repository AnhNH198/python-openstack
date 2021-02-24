class query:
    # query cpu
    # url = "https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/4/query"
    # params = {
    #     "db":"publicthor",
    #     "q": {
    #         "param":"value",
    #         "name2":"instances",
    #         "where":'("tags1" =~ /^{sid}$/ AND "tags2" = \'libvirt-kvm\' AND "tags3" = \'{name}\' AND "tags4" = \'total\' AND "tags5" = \'time\') AND time >= now() - 24h',
    #         "groupBy":'GROUP BY time(2m) fill(none)&epoch=ms',
    #         "isd":1
            
    #     }
    # }
    # queries = f'select ({params["q"]["param"]}) from "{params["q"]["name2"]}" where ("tags1" =~/^{["params"]["q"]["isd"]} $/ AND "tags2" = \'libvirt-kvm\') '
    # print(params["q"]["isd"])
 
    def query_cpu(sid, name, type=None):
        url = "https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/4/query"
        query = f'{url}?db=publicthor&q=SELECT mean("value") FROM "instances" WHERE ("tags1" =~ /^{sid}$/ AND "tags2" = \'libvirt-kvm\' AND "tags3" = \'{name}\' AND "tags4" = \'total\' AND "tags5" = \'time\') AND time >= now() - 24h GROUP BY time(2m) fill(none)&epoch=ms'
        return query
    
    # query memory
    def query_ram(sid, name, type=None):
        query = f'https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/4/query?db=publicthor&q=SELECT mean(\"value\") FROM \"instances\" WHERE (\"tags1\" =~ /^{sid}$/ AND \"tags2\" = \'libvirt-kvm\' AND \"tags3\" = \'{name}\' AND "tags4" = \'free\') AND time >= now() - 24h GROUP BY time(2m) fill(none)&epoch=ms'
        return query
    
    # query disk size
    def query_disk_size(sid, name, type=None):
        query = f'https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/4/query?db=publicthor&q=SELECT mean(\"value\") FROM \"instances\" WHERE (\"tags1\" =~ /^{sid}$/ AND "tags2" = \'libvirt-kvm\' AND \"tags3\" = \'{name}\' AND \"tags5\" = \'used-percent\') AND time >= now() - 24h GROUP BY time(2m), "tags4" fill(none)&epoch=ms'
        return query

    # query block read/write_bytes | iops
    def query_block_rw_iops(sid, name, type):
        query = f'https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/4/query?db=publicthor&q=SELECT mean(\"value\") FROM \"instances\" WHERE (\"tags1\" =~ /^{sid}$/ AND \"tags2\" = \'libvirt-kvm\' AND "tags3" = \'{name}\' AND \"tags4\" =~ /^(vda|vdb|vdc|vdd|vde|vdf|vdg|vdh|vdi)$/ AND \"tags5\" = \'{type}\') AND time >= now() - 24h GROUP BY time(2m), \"tags4\" fill(none)&epoch=ms'
        return query

    # Query net tx/rx_packets
    def query_net_tx_rx_pkt(sid, name, type):
        query = f'https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/4/query?db=publicthor&q=SELECT mean(\"value\") FROM \"instances\" WHERE (\"tags1\" =~ /^{sid}$/ AND \"tags2\" = \'libvirt-kvm\' AND "tags3" = \'{name}\' AND "tags4" =~ /^(eth0|eth1|eth2|eth3|eth4|eth5|eth6|eth7|eth8)$/ AND "tags5" = \'{type}\') AND time >= now() - 24h GROUP BY time(2m), \"tags4\", \"tags5\" fill(none)&epoch=ms'
        return query

    # Query net tx/rx_bytes
    def query_net_tx_rx_bytes(sid, name, type):
        query = f'https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/4/query?db=publicthor&q=SELECT mean("value") * 8 FROM "instances" WHERE ("tags1" =~ /^{sid}$/ AND "tags2" = \'libvirt-kvm\' AND "tags3" = \'{name}\' AND "tags4" =~ /^(eth0|eth1|eth2|eth3|eth4|eth5|eth6|eth7|eth8)$/ AND "tags5" = \'{type}\') AND time >= 1613602671298ms and time <= 1613604038387ms GROUP BY time(30s), "tags4" fill(none)&epoch=ms'
        return query
    def query_prometheus(sid, name=None, type=None):
        query = f'https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/18/api/v1/query_range?query=sum(node_cpu_info{{instance_id="{sid}"}})&start=1613688255&end=1613699055&step=120'

class queryLbs:
    def req_per_sec_frontend(lbid=None, frontend=None, backend_id=None, timefilter=None):
        query = f'https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/3/query?db=octavia&q=SELECT SUM("derivative") FROM ( SELECT derivative(mean("value"), 30s) FROM "servers" WHERE ("tags3" = \'haproxy\' AND "tags4" =~ /^{lbid}$/ AND "tags5" = \'frontend\' AND "tags6" =~ /^{frontend}$/ AND "tags7" = \'total\' AND "tags8" = \'req_tot\') AND time >= now() - {timefilter} GROUP BY time({time_interval}), "tags4", "tags6", "tags7", "tags2" )  GROUP BY time(30s)&epoch=ms'
        return query
    def status_code_frontend_2xx(lbid=None, frontend=None, backend_id=None, timefilter=None):
        query = f'https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/3/query?db=octavia&q=SELECT SUM("derivative") FROM (  SELECT derivative(mean("value"), 30s) FROM "servers" WHERE ("tags3" = \'haproxy\' AND "tags4" =~ /^{lbid}$/ AND "tags5" = \'frontend\' AND "tags6" =~ /^{frontend}$/ AND "tags7" = \'total\' AND "tags8" = \'hrsp_2xx\') AND time >= now() - {timefilter} GROUP BY time(30s), "tags5", "tags6", "tags7", "tags2", "tags8" fill(null)) GROUP BY time(30s);&epoch=ms'
        return query
    def status_code_frontend_3xx(lbid=None, frontend=None, backend_id=None, timefilter=None):
        query = f'https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/3/query?db=octavia&q=SELECT SUM("derivative") FROM ( SELECT derivative(mean("value"), 30s) FROM "servers" WHERE ("tags3" = \'haproxy\' AND "tags4" =~ /^{lbid}$/ AND "tags5" = \'frontend\' AND "tags6" =~ /^{frontend}$/ AND "tags7" = \'total\' AND "tags8" = \'hrsp_3xx\') AND time >= now() - {timefilter} GROUP BY time(30s), "tags5", "tags6", "tags7", "tags2", "tags8" fill(null) ) GROUP BY time(30s);&epoch=ms'
        return query
    def status_code_frontend_4xx(lbid=None, frontend=None, backend_id=None, timefilter=None):
        query = f'https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/3/query?db=octavia&q=SELECT SUM("derivative") FROM ( SELECT derivative(mean("value"), 30s) FROM "servers" WHERE ("tags3" = \'haproxy\' AND "tags4" =~ /^{lbid}$/ AND "tags5" = \'frontend\' AND "tags6" =~ /^{frontend}$/ AND "tags7" = \'total\' AND "tags8" = \'hrsp_4xx\') AND time >= now() - {timefilter} GROUP BY time(30s), "tags5", "tags6", "tags7", "tags2", "tags8" fill(null)) GROUP BY time(30s);&epoch=ms'
        return query
    def status_code_frontend_5xx(lbid=None, frontend=None, backend_id=None, timefilter=None):
        query = f'https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/3/query?db=octavia&q=SELECT SUM("derivative") FROM (  SELECT derivative(mean("value"), 30s) FROM "servers" WHERE ("tags3" = \'haproxy\' AND "tags4" =~ /^{lbid}$/ AND "tags5" = \'frontend\' AND "tags6" =~ /^{frontend}$/ AND "tags7" = \'total\' AND "tags8" = \'hrsp_5xx\') AND time >= now() - {timefilter} GROUP BY time(30s), "tags5", "tags6", "tags7", "tags2", "tags8" fill(null)) GROUP BY time(30s);&epoch=ms'
        return query
    def data_transfer_frontend_in(lbid=None, frontend=None, backend_id=None, timefilter=None):
        query = f'https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/3/query?db=octavia&q=SELECT SUM("derivative") FROM (SELECT derivative(mean("value"), 30s) FROM "servers" WHERE ("tags3" = \'haproxy\' AND "tags4" =~ /^{lbid}$/ AND "tags5" = \'frontend\' AND "tags6" =~ /^{frontend}$/ AND "tags7" = \'total\' AND "tags8" = \'bin\') AND time >= now() - {timefilter} GROUP BY time(1m), "tags2", "tags5", "tags6" fill(null) ) GROUP BY time(30s), "tags6";&epoch=ms'
        return query
    def data_transfer_frontend_out(lbid=None, frontend=None, backend_id=None, timefilter=None):
        query = f'https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/3/query?db=octavia&q=SELECT SUM("derivative") FROM ( SELECT derivative(mean("value"), 30s) FROM "servers" WHERE ("tags3" = \'haproxy\' AND "tags4" =~ /^{lbid}$/ AND "tags5" = \'frontend\' AND "tags6" =~ /^{frontend}$/ AND "tags7" = \'total\' AND "tags8" = \'bout\') AND time >= now() - {timefilter} GROUP BY time(30s), "tags2", "tags5", "tags6" fill(null) ) GROUP BY time(30s), "tags6";&epoch=ms'
        return query
    def req_per_sec_backend(lbid=None, frontend=None, backend_id=None, timefilter=None):
        query = f'https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/3/query?db=octavia&q=SELECT SUM("derivative") FROM (SELECT derivative(mean("value")) FROM "servers" WHERE ("tags3" = \'haproxy\' AND "tags4" =~ /^{lbid}$/ AND "tags5" = \'backend\' AND "tags6" =~ /^{backend_id}$/ AND "tags7" = \'total\' AND "tags8" = \'req_tot\') AND time >= now() - {timefilter} GROUP BY time(30s), "tags5", "tags6", "tags6", "tags2" fill(null) ) GROUP BY time(30s)&epoch=ms'
        return query
    def status_code_backend_2xx(lbid=None, frontend=None, backend_id=None, timefilter=None):
        query = f'https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/3/query?db=octavia&q=SELECT SUM("derivative") FROM (SELECT derivative(sum("value"), 30s) FROM "servers" WHERE ("tags3" = \'haproxy\' AND "tags4" =~ /^{lbid}$/ AND "tags5" = \'backend\' AND "tags6" =~ /^{backend_id}$/ AND "tags7" = \'total\' AND "tags8" = \'hrsp_2xx\') AND time >= now() - {timefilter} GROUP BY time(30s), "tags5", "tags6", "tags7", "tags2", "tags8" fill(null)) GROUP BY time(30s) OFFSET 1;&epoch=ms'
        return query
    def status_code_backend_3xx(lbid=None, frontend=None, backend_id=None, timefilter=None):
        query = f'https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/3/query?db=octavia&q=SELECT SUM("derivative") FROM ( SELECT derivative(sum("value"), 30s) FROM "servers" WHERE ("tags3" = \'haproxy\' AND "tags4" =~ /^{lbid}$/ AND "tags5" = \'backend\' AND "tags6" =~ /^{backend_id}$/ AND "tags7" = \'total\' AND "tags8" = \'hrsp_3xx\') AND time >= now() - {timefilter} GROUP BY time(30s), "tags5", "tags6", "tags7", "tags2" fill(null)  ) GROUP BY time(30s) OFFSET 1;&epoch=ms'
        return query
    def status_code_backend_4xx(lbid=None, frontend=None, backend_id=None, timefilter=None):
        query = f'https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/3/query?db=octavia&q=SELECT SUM("derivative") FROM ( SELECT derivative(sum("value"), 30s) FROM "servers" WHERE ("tags3" = \'haproxy\' AND "tags4" =~ /^{lbid}$/ AND "tags5" = \'backend\' AND "tags6" =~ /^{backend_id}$/ AND "tags7" = \'total\' AND "tags8" = \'hrsp_4xx\') AND time >= now() - {timefilter} GROUP BY time(30s), "tags5", "tags6", "tags7", "tags1" fill(null) ) GROUP BY time(30s) OFFSET 1;&epoch=ms'
        return query
    def status_code_backend_5xx(lbid=None, frontend=None, backend_id=None, timefilter=None):
        query = f'https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/3/query?db=octavia&q=SELECT SUM("derivative") FROM (SELECT derivative(sum("value"), 30s) FROM "servers" WHERE ("tags3" = \'haproxy\' AND "tags4" =~ /^{lbid}$/ AND "tags5" = \'backend\' AND "tags6" =~ /^{backend_id}$/ AND "tags7" = \'total\' AND "tags8" = \'hrsp_5xx\') AND time >= now() - {timefilter} GROUP BY time(30s), "tags5", "tags6", "tags7", "tags1" fill(null) ) GROUP BY time(30s) OFFSET 1;&epoch=ms'
        return query
    def data_transfer_backend_in(lbid=None, frontend=None, backend_id=None, timefilter=None):
        query = f'https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/3/query?db=octavia&q=SELECT SUM("derivative") FROM (SELECT derivative(sum("value"), 30s) FROM "servers" WHERE ("tags3" = \'haproxy\' AND "tags4" =~ /^{lbid}$/ AND "tags5" = \'backend\' AND "tags6" =~ /^{backend_id}$/ AND "tags7" = \'total\' AND "tags8" = \'bin\') AND time >= now() - {timefilter} GROUP BY time(30s), "tags5", "tags6", "tags6", "tags1" fill(null)  ) GROUP BY time(30s) OFFSET 1;&epoch=ms'
        return query
    def data_transfer_backend_out(lbid=None, frontend=None, backend_id=None, timefilter=None):
        query = f'https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/3/query?db=octavia&q=SELECT SUM("derivative") FROM (SELECT derivative(sum("value"), 30s) FROM "servers" WHERE ("tags3" = \'haproxy\' AND "tags4" =~ /^{lbid}$/ AND "tags5" = \'backend\' AND "tags6" =~ /^{backend_id}$/ AND "tags7" = \'total\' AND "tags8" = \'bout\') AND time >= now() - {timefilter} GROUP BY time(30s), "tags5", "tags6", "tags7", "tags2" fill(null)  ) GROUP BY time(30s) OFFSET 1;&epoch=ms'
        return query
    def downtime_backend(lbid=None, frontend=None, backend_id=None, timefilter=None):
        query = f'https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/3/query?db=octavia&q=SELECT SUM("mean") FROM (SELECT mean("value") FROM "servers" WHERE ("tags3" = \'haproxy\' AND "tags4" =~ /^{lbid}$/ AND "tags5" = \'backend\' AND "tags6" =~ /^{backend_id}$/ AND "tags8" = \'downtime\') AND time >= now() - {timefilter} GROUP BY time(1m), "tags5", "tags6", "tags7", "tags2" fill(null)) GROUP BY time(30s), "tags7" fill(null) OFFSET 1&epoch=ms'
        return query
    def queuesize_backend(lbid=None, frontend=None, backend_id=None, timefilter=None):
        query = f'https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/3/query?db=octavia&q=SELECT SUM("mean") FROM ( SELECT mean("value") FROM "servers" WHERE ("tags3" = \'haproxy\' AND "tags4" =~ /^{lbid}$/ AND "tags5" = \'backend\' AND "tags6" =~ /^{backend_id}$/ AND "tags8" = \'qcur\') AND time >= now() - {timefilter} GROUP BY time(30s), "tags5", "tags6", "tags7", "tags2" fill(null) ) GROUP BY time(30s), "tags7";&epoch=ms'
        return query
    def error_connection_per_second_backend(lbid=None, frontend=None, backend_id=None, timefilter=None, backend_server="All"):
        query = f'https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/3/query?db=octavia&q=SELECT mean("value") FROM "servers" WHERE ("tags1" =~ /^{lbid}$/ AND "tags3" = \'haproxy\' AND "tags5" = \'backend\' AND "tags6" =~ /^{backend_id}$/ AND "tags7" =~ /^{backend_server}$/ AND "tags8" = \'econ\') AND time >= now() - {timefilter} GROUP BY time(30s), "tags7" fill(null);&epoch=ms'
        return query
    def average_backend_response_time(lbid=None, frontend=None, backend_id=None, timefilter=None, backend_server="All"):
        query = f'https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/3/query?db=octavia&q=SELECT mean("value") FROM "servers" WHERE ("tags1" =~ /^{lbid}$/ AND "tags3" = \'haproxy\' AND "tags5" = \'backend\' AND "tags6" =~ /^{backend_id}$/ AND "tags7" =~ /^{backend_server}$/ AND "tags8" = \'rtime\') AND time >= now() - {timefilter} GROUP BY time(30s), "tags7" fill(null);&epoch=ms'
        return query
    def error_response_rate_backend(lbid=None, frontend=None, backend_id=None, timefilter=None):
        query = f'https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/3/query?db=octavia&q=SELECT mean("value") FROM "servers" WHERE ("tags1" =~ /^{lbid}$/ AND "tags3" = \'haproxy\' AND "tags5" = \'backend\' AND "tags6" =~ /^{backend_id}$/ AND "tags7" =~ /^()$/ AND "tags8" = \'eresp\') AND time >= now() - {timefilter} GROUP BY time(30s), "tags7" fill(null) OFFSET 1;&epoch=ms'
        return query
    def rate_session_per_second_backend(lbid=None, frontend=None, backend_id=None, timefilter=None):
        query = f'https://thor-hn-metrics-1.vccloud.vn:3000/api/datasources/proxy/3/query?db=octavia&q=SELECT mean("value") FROM "servers" WHERE ("tags1" =~ /^{lbid}$/ AND "tags3" = \'haproxy\' AND "tags5" = \'backend\' AND "tags6" =~ /^{backend_id}$/ AND "tags7" =~ /^()$/ AND "tags8" = \'rate\') AND time >= now() - {timefilter} GROUP BY time(30s), "tags7" fill(null);&epoch=ms'
        return query