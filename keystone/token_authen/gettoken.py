from keystone.token_authen.test import OS_AUTH_URL
from keystoneauth1.identity import v3
from keystoneauth1.session import Session

OS_AUTH_URL = ''
class createSession:
    def create_session(token, project_name):
        auth = v3.Token(
            auth_url= OS_AUTH_URL,
            token=token,
            project_name=project_name,
            project_domain_name='Default'
        )
        return Session(auth=auth)