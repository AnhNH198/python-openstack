dict = {
    'loadbalancer_id': ['529c45ae-cd57-4cbc-9973-94b7225f41b5'], 
    'frontend': ['089a17d6-48b9-42a2-9324-578518bd720f'], 
    'backend': ['7f62eb67-f6b9-4481-9a88-98b9f7cfce3c']
}
id = '529c45ae-cd57-4cbc-9973-94b7225f41b5'
for item in dict.get('loadbalancer_id'):
    if id in item:
        print("ok")