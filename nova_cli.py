from novaclient import client

class novaClient:
    def __init__(self, session, region):
        self.session = session
        self.region = region
    
    def nova(session, region):
        return client.Client("2", session=session, region_name=region)
    
    def list_server(session, region):
        list_servers = []
        nova = novaClient.nova(session, region)
        for info in nova.servers.list():
            # list_server.append(info.name)
            # list_server.append(info.addresses)
            # list_server.append(info.status)
            list_servers.append(info.id)
        return list_servers
