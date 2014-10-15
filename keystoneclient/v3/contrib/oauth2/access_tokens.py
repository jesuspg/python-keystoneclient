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

from __future__ import unicode_literals

from keystoneclient import base
from keystoneclient.v3.contrib.oauth2 import utils

try:
    from oauthlib import oauth2
except ImportError:
    oauth2 = None


class AccessToken(base.Resource):
    pass


class AccessTokenManager(base.CrudManager):
    """Manager class for manipulating identity OAuth access tokens."""
    resource_class = AccessToken

    def create(self, consumer_id, consumer_secret, authorization_code,
               redirect_uri):
        endpoint = utils.OAUTH2_PATH + '/access_token'

        url = self.client.auth_url.rstrip("/") + endpoint
        headers, body = self._generate_json_request(consumer_id, consumer_secret, 
                                                    authorization_code, redirect_uri)

        resp, body = self.client.post(endpoint, headers=headers, body=body)
        token = utils.get_oauth_token_from_body(resp.content)
        return self.resource_class(self, token)

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
            'Authorization': self._http_basic(consumer_id,consumer_secret)
        }
        return headers, body

    def _http_basic(self, consumer_id, consumer_secret):
        auth_string = consumer_id + ':' + consumer_secret
        return 'Basic ' + auth_string.encode('base64')