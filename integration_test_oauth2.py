# TODO(garcianavalon) make proper integration tests
from keystoneclient.v3 import client

keystone = client.Client(token='ADMIN',endpoint='http://127.0.0.1:5000/v3')

redirect_uri='https://testuri.com'
scope='all'
scopes=[scope]
user_id=1

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
keystone.oauth2.access_tokens.create(consumer_id=consumer_id,
                                    authorization_code=authorization_code.code,
                                    redirect_uri=redirect_uri,
                                    consumer_secret=consumer_secret)
