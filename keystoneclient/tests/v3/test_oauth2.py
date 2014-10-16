# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import urllib
import uuid
import mock
import six
from six.moves.urllib import parse as urlparse
from testtools import matchers

from keystoneclient import session
from keystoneclient.openstack.common import timeutils
from keystoneclient.tests.v3 import client_fixtures
from keystoneclient.tests.v3 import utils
from keystoneclient.v3.contrib.oauth2 import auth
from keystoneclient.v3.contrib.oauth2 import access_tokens
from keystoneclient.v3.contrib.oauth2 import authorization_codes
from keystoneclient.v3.contrib.oauth2 import consumers


class ConsumerTests(utils.TestCase, utils.CrudTests):

    DEFAULT_REDIRECT_URIS = ['https://uri.com']
    DEFAULT_SCOPES = ['all_info']
    DEFAULT_CLIENT_TYPE='confidential'
    DEFAULT_GRANT_TYPE='authorization_code'

    def setUp(self):
        super(ConsumerTests, self).setUp()
        self.key = 'consumer'
        self.collection_key = 'consumers'
        self.model = consumers.Consumer
        self.manager = self.client.oauth2.consumers
        self.path_prefix = 'OS-OAUTH2'

    def new_ref(self, **kwargs):
        kwargs = super(ConsumerTests, self).new_ref(**kwargs)
        kwargs.setdefault('description', uuid.uuid4().hex)
        kwargs.setdefault('client_type', self.DEFAULT_CLIENT_TYPE)
        kwargs.setdefault('redirect_uris', self.DEFAULT_REDIRECT_URIS)
        kwargs.setdefault('scopes', self.DEFAULT_SCOPES)
        kwargs.setdefault('grant_type', self.DEFAULT_GRANT_TYPE)
        return kwargs

    def _consumer_data(self, description=None, 
                        client_type=DEFAULT_CLIENT_TYPE,
                        redirect_uris=DEFAULT_REDIRECT_URIS,
                        grant_type=DEFAULT_GRANT_TYPE,
                        scopes=DEFAULT_SCOPES):
        data = {
            'consumer': {
                'description': description,
                'client_type': client_type,
                'redirect_uris': redirect_uris,
                'grant_type': grant_type,
                'scopes': scopes
            }
        }
        return data

    def _create_consumer(self, consumer_data):
        self.stub_url('POST',
                    [self.path_prefix, self.collection_key],
                    status_code=201, json=consumer_data)

        consumer = self.manager.create()
        return consumer

    def test_create_consumer_defaults(self):
        consumer_data = self._consumer_data()
        consumer = self._create_consumer(consumer_data)
        self.assertEqual(self.DEFAULT_CLIENT_TYPE, consumer.client_type)
        #self.assertIsNotNone(consumer.id)
        self.assertIsNone(consumer.description)



class AuthorizationCodeTests(utils.TestCase):


    def setUp(self):
        super(AuthorizationCodeTests, self).setUp()
        self.model = authorization_codes.AuthorizationCode
        self.manager = self.client.oauth2.authorization_codes
        self.path_prefix = 'OS-OAUTH2'

    def test_authorize(self):
        stub_headers = {
            'Location':'https://foo.com/welcome_back?code=somerandomstring&state=xyz'
        }
        self.stub_url('POST',
                      [self.path_prefix, 'authorize',], 
                      status_code=200,headers=stub_headers)

        
        user_id = uuid.uuid4().hex
        consumer_id = uuid.uuid4().hex
        scopes = [uuid.uuid4().hex]

        # Assert the manager is returning the expected data
        authorization_code = self.manager.authorize(
                                        user=user_id, 
                                        consumer=consumer_id, 
                                        scopes=scopes)

        self.assertIsNotNone(authorization_code.code)
        self.assertIsNotNone(authorization_code.state)
        self.assertIsNotNone(authorization_code.redirect_uri)

        # Assert that the request was sent in the expected structure
        expected_body = {
            'user_auth': {
                'client_id':consumer_id,
                'user_id':user_id,
                'scopes':scopes
            }
        }
        self.assertRequestBodyIs(json=expected_body)

    def test_request_authorization(self):
        scope = [uuid.uuid4().hex]
        consumer_id = uuid.uuid4().hex
        redirect_uri = uuid.uuid4().hex
        state = uuid.uuid4().hex

        # NOTE(garcianavalon) we use a list of tuples to ensure param order
        # in the query string
        stub_credentials = [
            ('response_type','code'),
            ('client_id',consumer_id),
            ('redirect_uri',redirect_uri),
            ('scope',scope),
            ('state',state)
        ]
        query_string = '?%s' %urllib.urlencode(stub_credentials)

        # NOTE(garcianavalon) this JSON emulates the provider response body
        # but it might not be up-to-date because it's changing continuosly
        # during development to adjust to different needs that keep appearing.
        # Only take it as mean to test that the request_authorization call
        # returns a dict, to know more about the response body check the Keystone
        # OAuth2 Extension documentation
        stub_body = { 
            'data': {
                'consumer': {
                    'id':consumer_id
                },
                'redirect_uri':redirect_uri,
                'requested_scopes':scope
            }
        }

        self.stub_url('GET', [self.path_prefix, 'authorize', query_string],
                      status_code=201,json=stub_body)

        # Assert the manager is returning a dict with the info from the server
        response_body =  self.manager.request_authorization(
                                            consumer=consumer_id,
                                            redirect_uri=redirect_uri,
                                            scope=scope,
                                            state=state)

        assert(isinstance(response_body,dict))
        


class AuthenticateWithOAuthTests(utils.TestCase):


    def test_oauth_authenticate_success(self):
        access_token = uuid.uuid4().hex

        # Just use an existing project scoped token and change
        # the methods to oauth2, and add its section.
        oauth_token = client_fixtures.project_scoped_token()
        oauth_token['methods'] = ["oauth2"]
        oauth_token['oauth2'] = {
            "access_token_id": access_token
        }
        self.stub_auth(json=oauth_token)

        a = auth.OAuth(self.TEST_URL, access_token=access_token)
        s = session.Session(auth=a)
        t = s.get_token()
        self.assertEqual(self.TEST_TOKEN, t)
