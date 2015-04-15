# Copyright (C) 2014 Universidad Politecnica de Madrid
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import json

from keystoneclient import base
from keystoneclient import exceptions
from keystoneclient.v3.contrib.oauth2 import utils

class AccessToken(base.Resource):
    pass


class AccessTokenManager(base.CrudManager):
    """Manager class for manipulating identity OAuth access tokens."""
    resource_class = AccessToken
    collection_key = 'access_tokens'
    key = 'access_token'
    base_url = utils.OAUTH2_PATH

    def create(self, consumer_id, consumer_secret, authorization_code,
               redirect_uri):
        endpoint = self.base_url + '/access_token'

        headers, body = self._generate_json_request(consumer_id, consumer_secret, 
                                                    authorization_code, redirect_uri)

        resp, body = self.client.post(endpoint, headers=headers, body=body)

        token = json.loads(resp.content)
        return self.resource_class(self, token)

    def list_for_user(self, user, **kwargs):
        """lists all the created access token for a user."""
        base_url = '/users/{0}'.format(base.getid(user)) + self.base_url
        return super(AccessTokenManager, self).list(
            base_url=base_url, **kwargs)

    def list(self, **kwargs):
        raise exceptions.MethodNotImplemented(
            'List not supported for access_tokens')

    def update(self, **kwargs):
        raise exceptions.MethodNotImplemented(
            'Update not supported for access_tokens')

    def get(self, **kwargs):
        raise exceptions.MethodNotImplemented(
            'Get not supported for access_tokens')

    def find(self, **kwargs):
        raise exceptions.MethodNotImplemented(
            'Find not supported for access_tokens')

    def put(self, **kwargs):
        raise exceptions.MethodNotImplemented(
            'Put not supported for access_tokens')

    def delete(self, **kwargs):
        raise exceptions.MethodNotImplemented(
            'Delete not supported for access_tokens')

    def _generate_json_request(self, consumer_id, consumer_secret,
                                authorization_code, redirect_uri):
        body = {
            'token_request' : {
                'grant_type':'authorization_code',
                'code': authorization_code,
                'redirect_uri':redirect_uri
            }
        }    
        headers = {
            'Authorization': self._http_basic(consumer_id, consumer_secret)
        }
        return headers, body

    def _http_basic(self, consumer_id, consumer_secret):
        auth_string = consumer_id + ':' + consumer_secret
        return 'Basic ' + base64.b64encode(auth_string)

