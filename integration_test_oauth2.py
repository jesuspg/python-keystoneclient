# TODO(garcianavalon) make proper integration tests
from keystoneclient.v3 import client
from keystoneclient import session
from keystoneclient.v3.contrib.oauth2 import auth
url = 'http://127.0.0.1:5000/v3'
keystone = client.Client(token='ADMIN',endpoint=url)

redirect_uri='https://testuri.com'
scope='all_info'
scopes=[scope]
admin_user = keystone.users.find(name='admin')
user_id=admin_user.id

#create a consumer
consumer = keystone.oauth2.consumers.create(client_type='confidential',
                                            redirect_uris=[redirect_uri],
                                            grant_type='authorization_code', 
                                            scopes=scopes)
consumer_id = consumer.id
consumer_secret = consumer.secret

#store credentials
keystone.oauth2.authorization_codes.request_authorization(consumer=consumer_id,
                                                        redirect_uri=redirect_uri, 
                                                        scope=scope)
#grant authorization
authorization_code = keystone.oauth2.authorization_codes.authorize(user=user_id, 
                                            consumer=consumer_id, 
                                            scopes=scopes)
#get an access token
access_token = keystone.oauth2.access_tokens.create(consumer_id=consumer_id,
                                    authorization_code=authorization_code.code,
                                    redirect_uri=redirect_uri,
                                    consumer_secret=consumer_secret)
# log in and get a keystone token
a = auth.OAuth2(url,access_token=access_token.access_token)
s = session.Session(auth=a)
keystone = client.Client(session=s)
keystone.users.list()
