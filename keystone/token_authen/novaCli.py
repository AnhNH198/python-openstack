from novaclient import client

class novaClient:
    def __init__(self, session, region):
        self.session = session
        self.region = region
    def nova(session, region):
        return client.Client("2", session=session, region_name=region)