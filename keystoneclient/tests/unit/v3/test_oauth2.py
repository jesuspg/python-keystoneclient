# Copyright (C) 2014 Universidad Politecnica de Madrid
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

import base64
import urllib
import uuid

from keystoneclient import exceptions
from keystoneclient import session
from keystoneclient.tests.unit.v3 import client_fixtures
from keystoneclient.tests.unit.v3 import utils
from keystoneclient.v3.contrib.oauth2 import auth
from keystoneclient.v3.contrib.oauth2 import access_tokens
from keystoneclient.v3.contrib.oauth2 import authorization_codes
from keystoneclient.v3.contrib.oauth2 import consumers


class ConsumerTests(utils.TestCase, utils.CrudTests):

    DEFAULT_REDIRECT_URIS = ['https://uri.com']
    DEFAULT_SCOPES = ['all_info']
    DEFAULT_CLIENT_TYPE = 'confidential'
    DEFAULT_GRANT_TYPE = 'authorization_code'

    def setUp(self):
        super(ConsumerTests, self).setUp()
        self.key = 'consumer'
        self.collection_key = 'consumers'
        self.model = consumers.Consumer
        self.manager = self.client.oauth2.consumers
        self.path_prefix = 'OS-OAUTH2'

    def new_ref(self, **kwargs):
        kwargs = super(ConsumerTests, self).new_ref(**kwargs)
        kwargs.setdefault('name', uuid.uuid4().hex)
        kwargs.setdefault('description', uuid.uuid4().hex)
        kwargs.setdefault('client_type', self.DEFAULT_CLIENT_TYPE)
        kwargs.setdefault('redirect_uris', self.DEFAULT_REDIRECT_URIS)
        kwargs.setdefault('scopes', self.DEFAULT_SCOPES)
        kwargs.setdefault('grant_type', self.DEFAULT_GRANT_TYPE)
        return kwargs

    def _consumer_data(self, name=None, description=None, 
                        client_type=DEFAULT_CLIENT_TYPE,
                        redirect_uris=DEFAULT_REDIRECT_URIS,
                        grant_type=DEFAULT_GRANT_TYPE,
                        scopes=DEFAULT_SCOPES):
        if not name:
            name = uuid.uuid4().hex
        data = {
            'consumer': {
                'name': name,
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

        consumer = self.manager.create(uuid.uuid4().hex)
        return consumer

    def test_create_consumer_defaults(self):
        consumer_data = self._consumer_data()
        consumer = self._create_consumer(consumer_data)
        self.assertEqual(self.DEFAULT_CLIENT_TYPE, consumer.client_type)
        #self.assertIsNotNone(consumer.id)
        self.assertIsNone(consumer.description)

    def test_list_consumers_by_user(self):
        user_id = uuid.uuid4().hex
        ref_list = [self.new_ref(), self.new_ref()]

        self.stub_entity('GET',
                      parts=['users', user_id, 
                        self.path_prefix, self.collection_key],
                      entity=ref_list)

        returned_list = self.manager.list(user=user_id)

        self.assertEqual(len(ref_list), len(returned_list))
        for item in returned_list:
            self.assertIsInstance(item, self.model)



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
                      status_code=200, headers=stub_headers)

        consumer_id = uuid.uuid4().hex
        scopes = [uuid.uuid4().hex]

        # Assert the manager is returning the expected data

        authorization_code = self.manager.authorize( 
                                        consumer=consumer_id, 
                                        scopes=scopes)

        self.assertIsNotNone(authorization_code.code)
        self.assertIsNotNone(authorization_code.state)
        self.assertIsNotNone(authorization_code.redirect_uri)

        # Assert that the request was sent in the expected structure
        expected_body = {
            'user_auth': {
                'client_id':consumer_id,
                'scopes':scopes
            }
        }
        self.assertRequestBodyIs(json=expected_body)

    def test_request_authorization(self):
        scope = [uuid.uuid4().hex]
        consumer_id = uuid.uuid4().hex
        redirect_uri = uuid.uuid4().hex
        state = uuid.uuid4().hex

        scope_string = ' '.join(scope)
        # NOTE(garcianavalon) we use a list of tuples to ensure param order
        # in the query string
        stub_credentials = [
            ('response_type', 'code'),
            ('client_id', consumer_id),
            ('redirect_uri', redirect_uri),
            ('scope', scope_string),
            ('state', state)
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
                      status_code=201, json=stub_body)

        # Assert the manager is returning a dict with the info from the server
        response_body = self.manager.request_authorization(
                                            consumer=consumer_id,
                                            redirect_uri=redirect_uri,
                                            scope=scope,
                                            state=state)

        assert(isinstance(response_body, dict))
        

class AccessTokenTests(utils.TestCase, utils.CrudTests):


    def setUp(self):
        super(AccessTokenTests, self).setUp()
        self.manager = self.client.oauth2.access_tokens
        self.model = access_tokens.AccessToken
        self.path_prefix = 'OS-OAUTH2'
        self.key = 'access_token'
        self.collection_key = 'access_tokens'

    def test_create(self):
        consumer_id = uuid.uuid4().hex
        consumer_secret = uuid.uuid4().hex
        redirect_uri = uuid.uuid4().hex
        authorization_code = uuid.uuid4().hex

        stub_body = {
            'access_token': uuid.uuid4().hex,
            'refresh_token': uuid.uuid4().hex,
            'expires_in': 3600,
            'scope': ' '.join([uuid.uuid4().hex, uuid.uuid4().hex]),
            'token_type': 'Bearer'
        }
        self.stub_url('POST', [self.path_prefix, 'access_token'],
                      status_code=201, json=stub_body)

        # Assert that the manager creates an access token object
        access_token = self.manager.create(consumer_id=consumer_id, 
                                        consumer_secret=consumer_secret,
                                        authorization_code=authorization_code, 
                                        redirect_uri=redirect_uri)

        self.assertIsInstance(access_token, self.model)
        self.assertIsNotNone(access_token.access_token)
        self.assertIsNotNone(access_token.scope)
        self.assertIsNotNone(access_token.expires_in)

        # Assert that the request was sent in the expected structure
        expected_body = {
            'token_request' : {
                'grant_type':'authorization_code',
                'code': authorization_code,
                'redirect_uri':redirect_uri
            }
        }
        self.assertRequestBodyIs(json=expected_body)

        auth_string = consumer_id + ':' + consumer_secret
        expected_auth = 'Basic ' + base64.b64encode(auth_string)
        self.assertRequestHeaderEqual('Authorization', expected_auth)

    def test_list_for_user(self):
        user_id = uuid.uuid4().hex
        access_tokens_ref = {
            'access_tokens': [
                {
                    'id': uuid.uuid4().hex,
                },
                {
                    'id': uuid.uuid4().hex,
                },
            ]
        }
        self.stub_url('GET',
                      [self.path_prefix, 'users', user_id,
                       self.collection_key],
                       status_code=204,
                       json=access_tokens_ref)

        result = self.manager.list_for_user(user=user_id)

        self.assertEqual(len(access_tokens_ref['access_tokens']), 
                         len(result))

    def test_list_params(self):
        # list not supported for access tokens
        self.assertRaises(exceptions.MethodNotImplemented, self.manager.list)

    def test_list(self):
        # list not supported for access tokens
        self.assertRaises(exceptions.MethodNotImplemented, self.manager.list)

    def test_update(self):
        # Update not supported for access tokens
        self.assertRaises(exceptions.MethodNotImplemented, self.manager.update)

    def test_delete(self):
        # Delete not supported for access tokens
        self.assertRaises(exceptions.MethodNotImplemented, self.manager.delete)

    def test_get(self):
        # Get not supported for access tokens
        self.assertRaises(exceptions.MethodNotImplemented, self.manager.get)

    def test_find(self):
        # Find not supported for access tokens
        self.assertRaises(exceptions.MethodNotImplemented, self.manager.find)

class AuthenticateWithOAuthTests(utils.TestCase):


    def test_oauth_authenticate_success(self):
        access_token = uuid.uuid4().hex

        # Just use an existing project scoped token and change
        # the methods to oauth2, and add its section.
        oauth_token = client_fixtures.unscoped_token()

        oauth_token['methods'] = ["oauth2"]
        oauth_token['oauth2'] = {
            "access_token_id": access_token
        }
        self.stub_auth(json=oauth_token)

        a = auth.OAuth2(self.TEST_URL, access_token=access_token)
        s = session.Session(auth=a)
        t = s.get_token()
        self.assertEqual(self.TEST_TOKEN, t)

        OAUTH2_REQUEST_BODY = {
            "auth": {
                "identity": {
                    "methods": ["oauth2"],
                    "oauth2": {
                        "access_token_id": access_token
                    }
                }
            }
        }

        self.assertRequestBodyIs(json=OAUTH2_REQUEST_BODY)

    def test_oauth_authenticate_scoped_success(self):

        access_token = uuid.uuid4().hex

        # Just use an existing project scoped token and change
        # the methods to oauth2, and add its section.
        oauth_token = client_fixtures.project_scoped_token()
        oauth_token['methods'] = ["oauth2"]
        oauth_token['oauth2'] = {
            "access_token_id": access_token
        }
        self.stub_auth(json=oauth_token)

        a = auth.OAuth2(self.TEST_URL, access_token=access_token)
        s = session.Session(auth=a)
        t = s.get_token()
        self.assertEqual(self.TEST_TOKEN, t)

        OAUTH2_REQUEST_BODY = {
            "auth": {
                "identity": {
                    "methods": ["oauth2"],
                    "oauth2": {
                        "access_token_id": access_token
                    }
                }
            }
        }

        self.assertRequestBodyIs(json=OAUTH2_REQUEST_BODY)
