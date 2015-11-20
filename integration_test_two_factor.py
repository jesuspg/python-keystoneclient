from keystoneclient.v3 import client
from keystoneclient import session
from keystoneclient.auth.identity import v3

from keystoneclient.v3.contrib.two_factor import auth as authentication
url = 'http://127.0.0.1:5000/v3'

def fiwareclient(session=None, request=None):# TODO(garcianavalon) use this
    """Encapsulates all the logic for communicating with the modified keystone server.

    The IdM has its own admin account in the keystone server, and uses it to perform
    operations like create users, projects, etc. when there is no user with admin rights
    (for example, when user registration) to overcome the Keystone limitations.

    Also adds the methods to operate with the OAuth2.0 extension.
    """
    # TODO(garcianavalon) find a way to integrate this with the existng keystone api
    # TODO(garcianavalon)caching and efficiency with the client object.
    if not session:
        session = _two_factor_session(user='idm', password='idm')
    keystone = client.Client(session=session)
    return keystone

def _password_session():
    auth = v3.Password(auth_url="http://localhost:5000/v3",
                       user_id='idm',
                       password='idm',
                       project_name='idm',
                       project_domain_id='default')
    return session.Session(auth=auth)

def _two_factor_session(user, password, verification_code=None, project='idm', project_domain_id='default'):
    auth = authentication.TwoFactor(auth_url="http://localhost:5000/v3",
                        user_id=user,
                        password=password,
                        verification_code=verification_code,
                        user_domain_name=domain,
                        user_domain_id=project_domain_id)

keystone = fiwareclient()

# RUN fab keystone.test_data

keystone.two_factor.keys.generate_new_key(user='user0', security_question='Who?', security_answer='Me!')
print("Created key for user0.")

if keystone.two_factor.keys.check_activated_two_factor(user='user0'):
    print("Two factor is enabled for user0!")



keystone.two_factor.keys.deactivate_two_factor(user='user0')
print("Disabling two factor.")

if not keystone.two_factor.keys.check_activated_two_factor(user='user0'):
    print("Two factor is disableed for user0!")