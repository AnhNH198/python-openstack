
import os

from flask import g


from keystoneauth1.identity import v3
from keystoneauth1.session import Session
from keystoneclient.v3 import client as keystone_client


from config import config

from utils.caching import tmpl_cache
from utils.constants import APPLICATION_CREDENTIAL


env = os.environ.get('ENV', 'development')
CONF = config[env]

def create_session(auth_method=CONF.DEFAULT_USER_AUTH_METHOD, **credentials):
    def callback():
        if auth_method == CONF.DEFAULT_USER_AUTH_METHOD:
            d = {
                "project_name": credentials.get("project_name"),
                "project_domain_name": CONF.OS_PROJECT_DOMAIN_NAME
            }
            if credentials.get("project_id"):
                d['project_id'] = credentials.get("project_id")

            if not credentials.get("trust_id"):
                auth = v3.Token(
                    auth_url=CONF.OS_AUTH_URL,
                    token=credentials.get("token"), **d
                )
            else:
                auth = v3.Token(
                    auth_url=CONF.OS_AUTH_URL,
                    token=credentials.get("token"),
                    trust_id=credentials.get("trust_id")
                )
            return Session(auth=auth)

        if auth_method == APPLICATION_CREDENTIAL:
            auth = v3.ApplicationCredential(
                auth_url=CONF.OS_AUTH_URL,
                **credentials
            )
            return Session(auth=auth)

    if auth_method == CONF.DEFAULT_USER_AUTH_METHOD:
        return tmpl_cache.get(
            key="%s-%s-%s-%s-%s" % (
                auth_method,
                credentials.get("token"),
                credentials.get("project_name"),
                credentials.get("project_id"),
                credentials.get("trust_id"),
            ),
            createfunc=callback
        )
    elif auth_method == APPLICATION_CREDENTIAL:
        return tmpl_cache.get(
            key="%s-%s-%s" % (
                auth_method,
                credentials.get("application_credential_id"),
                credentials.get("application_credential_name")
            ),
            createfunc=callback
        )