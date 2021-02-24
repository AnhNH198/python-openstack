from octaviaclient.api.v2.octavia import OctaviaAPI

class octaviCli():
    def __init__(self, urls, region):
        self.urls = urls
        self.region = region
    def list_lbs(self, sess):
        dict = {"loadbalancer_id":[],"frontend":[],"backend":[]}
        client = OctaviaAPI(
            self.urls,
            region_name=self.region,
            session=sess
        )

        # Get ID of loadbalancer | listeners, pools belong to loadbalancer
        info = client.load_balancer_list()
        for items in info.get('loadbalancers', {}):
            dict["loadbalancer_id"].append(items.get('id'))
            for item in items.get('listeners'):
                dict["frontend"].append(item.get('id'))
            for item in items.get('pools'):
                dict['backend'].append(item.get('id')) 
        return dict