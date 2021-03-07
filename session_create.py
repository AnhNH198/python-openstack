from keystoneauth1.identity import v3
from keystoneauth1.session import Session
from keystoneclient.v3 import client

auth = v3.Password(auth_url='', \
                    username='@.vn', \
                    password='', \
                    user_domain_name='Default', \
                    project_domain_name='Default')

sess = Session(auth=auth)
ks = client.Client(session=sess)

print("token: ", sess.get_token())

print(sess.get_auth_headers())

print(sess.get_project_id())