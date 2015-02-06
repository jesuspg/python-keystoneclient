from keystoneclient.v3 import client
from keystoneclient import session
from keystoneclient.v3.contrib.oauth2 import auth
from keystoneclient.auth.identity import v3

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
        session = _password_session()
    keystone = client.Client(session=session)
    return keystone

def _password_session():
    auth = v3.Password(auth_url="http://localhost:5000/v3",
                       username='idm',
                       password='idm',
                       project_name='idm',
                       user_domain_id='default',
                       project_domain_id='default')
    return session.Session(auth=auth)

keystone = fiwareclient()

#Registrer User:
if 0:
	new_user = keystone.user_registration.users.register_user(name='Test User',
															  domain='default',
															  password='test',
															  email='user@test.com')

	print ('\nUser activated? ')
	print new_user.enabled

#Activate User
if 0:
	activated_user = keystone.user_registration.users.activate_user(new_user.id, new_user.activation_key)

	print ('\nUser activated? ')
	print activated_user.enabled

#Forgot Password
if 0: 
	token = keystone.user_registration.token.get_reset_token(new_user.id)
	print token

	user = keystone.user_registration.users.reset_password(new_user, token.id, 'newpassword')
	print user

#Delete created user and associated project
if 0:
	keystone.users.delete(new_user.id)
	project = keystone.projects.find(name=new_user.name)
	keystone.projects.delete(project.id)

#New Activation Key
# The new activation key does not work in these tests.
if 1:
	user_reset = keystone.user_registration.users.register_user(name='Test User',
															  domain='default',
															  password='test',
															  email='user@test.com')
	project = keystone.projects.find(name=user_reset.name)
	print user_reset.id
	print project.id
	print ('\nUser activated? ')
	print user_reset.enabled

	print user_reset.activation_key

	new_activation_key = keystone.user_registration.activation_key.new_activation_key(user_reset.id)
	print new_activation_key.id
	print user_reset.activation_key

	activated_user = keystone.user_registration.users.activate_user(user_reset.id, new_activation_key.id)
	print activated_user

	print ('\nUser activated? ')
	print user_reset.enabled

	keystone.users.delete(user_reset.id)
	# project = keystone.projects.find(name=user_reset.name)
	keystone.projects.delete(project.id)


