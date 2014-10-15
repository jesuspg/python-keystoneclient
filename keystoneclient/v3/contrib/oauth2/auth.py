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

from keystoneclient.auth.identity import v3
try:
    from oauthlib import oauth2
except ImportError:
    oauth2 = None

class OAuthMethod(v3.AuthMethod):
    _method_parameters = ['access_token']

    def __init__(self, **kwargs):
        """Construct an OAuth based authentication method.
        :param string consumer_key: Consumer key.
        :param string consumer_secret: Consumer secret.
        :param string access_key: Access token key.
        :param string access_secret: Access token secret.
        """
        super(OAuthMethod, self).__init__(**kwargs)
        if oauth2 is None:
            raise NotImplementedError('optional package oauthlib'
        ' is not installed')

    def get_auth_data(self, session, auth, headers, **kwargs):
        # Build the data for our custom auth method. Check the OAuth2.0 keystone
        # auth plugin for more info: https://www.github.com/ging/keystone
        auth_data = {
            'access_token_id':self.access_token
        }
        name = 'oauth2'
        return name, auth_data


class OAuth(v3.AuthConstructor):
    _auth_method_class = OAuthMethod