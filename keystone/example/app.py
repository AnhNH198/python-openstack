from flask import g
from flask import request
 
 g.auth_method = request.headers.get("X-Auth-Type", SESSION)
    g.region_name = request.headers.get('X-Region-Name', CONF.OS_REGION_NAME)
    if 'region_name' in request.args:
        g.region_name = request.args.get('region_name')

    if g.region_name not in CONF.OS_SYSTEM_REGION_NAME:
        abort(404, 'Region Name not found')

    # Temp by pass
    if request.headers.get('X-Auth-Token'):
        g.auth_method = CONF.DEFAULT_USER_AUTH_METHOD

    if g.auth_method == APPLICATION_CREDENTIAL:
        g.ac_id = request.headers.get("X-App-Credential-Id")
        g.ac_name = request.headers.get("X-App-Credential-Name")
        g.ac_secret = request.headers.get("X-App-Credential-Secret")
    elif g.auth_method == CONF.DEFAULT_USER_AUTH_METHOD:
        g.token = request.headers.get('X-Auth-Token')
    elif g.auth_method != SESSION:
        abort(401, "%s is unsupported" % g.auth_method)

    g.trust_id = None
    if request.headers.get('X-Trust-Id'):
        g.trust_id = request.headers.get('X-Trust-Id')

    tenant_id = None
    project_name = None
    if g.auth_method == APPLICATION_CREDENTIAL:
        if not (g.ac_id and g.ac_secret):
            abort(401)
    elif g.auth_method == CONF.DEFAULT_USER_AUTH_METHOD:
        # Kiem tra + lay email, tenant cua user
        if request.headers.get('X-Tenant-Name'):
            project_name = request.headers.get('X-Tenant-Name')
        elif request.headers.get('X-Tenant-Id'):
            tenant_id = request.headers.get('X-Tenant-Id')
        else:
            abort(401)
    else:
        # Su dung.sessionion
        if 'session' not in request.cookies:
            app.logger.debug('Missing Session Cookie.')
            abort(401, _('Missing authentication info.'))

        try:
            serializer = app.config['COOKIE_SERIALIZER']
            user_info = serializer.loads(request.cookies['session'])
            project_name = user_info['tenant_name']
            g.token = user_info['token']
        except BadSignature:
            app.logger.debug('Unable to decrypt Session Cookie value: {}'
                             .format(request.cookies['session']))
            abort(401, _('Invalid Session Cookie.'))
        except Exception as e:
            app.logger.error(str(e))
            abort(401, str(e))

    if g.auth_method != APPLICATION_CREDENTIAL and \
            not (project_name or tenant_id):
        app.logger.error("Missing Project Name")
        abort(401)

    # Make credentials and check valid
    if g.auth_method == APPLICATION_CREDENTIAL:
        g.credentials = {
            'auth_method': g.auth_method,
            'application_credential_id': g.ac_id,
            'application_credential_name': g.ac_name,
            'application_credential_secret': g.ac_secret,
        }
    else:
        g.credentials = {
            'auth_method': CONF.DEFAULT_USER_AUTH_METHOD,
            'project_id': tenant_id,
            'project_name': project_name,
            'token': g.token,
            'trust_id': g.trust_id,
        }

    g.session = create_session(**g.credentials)