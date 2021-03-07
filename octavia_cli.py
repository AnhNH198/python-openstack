from octaviaclient.api.v2.octavia import OctaviaAPI

class octaviCli():
    def __init__(self, url, region_name):
        self.url = url
        self.region_name = region_name
    def list_lbs(self, sess):
        dict = {"loadbalancer_id":[],"frontend":[],"Backend":[]}
        client = OctaviaAPI(
            self.url,
            region_name=self.region_name,
            session=sess
        )
        info = client.load_balancer_list()
        for items in info.get('loadbalancers', {}):
            dict["loadbalancer_id"].append(items.get('id'))
            for item in items.get('listeners'):
                dict["frontend"].append(item.get('id'))
            for item in items.get('pools'):
                dict['Backend'].append(item.get('id')) 
        return dict