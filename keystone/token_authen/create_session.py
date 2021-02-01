from keystoneauth1.identity import v3
from keystoneauth1.session import Session

class create_session():
    def create_session(token, project_name):
        auth = v3.Token(
            auth_url= OS_AUTH_URL,
            token=token,
            project_name=project_name,
            project_domain_name='Default'
        )
        return Session(auth=auth)