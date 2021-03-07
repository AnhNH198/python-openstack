from keystoneauth1.identity import v3
from keystoneauth1.session import Session

class createSession:
    def __init__(self, auth_url, token, project_name, project_domain_name='Default'):
        self.auth_url = auth_url
        self.token = token
        self.project_name = project_name
        self.project_domain_name = project_domain_name

    def create_session(auth_url, token, project_name, project_domain_name='Default'):
        auth = v3.Token(
            auth_url= auth_url,
            token=token,
            project_name=project_name,
            project_domain_name=project_domain_name
        )
        return Session(auth=auth)