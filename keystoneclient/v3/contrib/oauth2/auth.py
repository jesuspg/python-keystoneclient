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


class OAuth2Method(v3.AuthMethod):

    _method_parameters = ['access_token']

    def __init__(self, **kwargs):
        """Construct an OAuth based authentication method.
        :param string access_token: Access token id.
        """
        super(OAuth2Method, self).__init__(**kwargs)


    def get_auth_data(self, session, auth, headers, **kwargs):
        # Build the data for our custom auth method. Check the OAuth2.0 keystone
        # auth plugin for more info: https://www.github.com/ging/keystone
        auth_data = {
            'access_token_id':self.access_token
        }
        name = 'oauth2'
        return name, auth_data


class OAuth2(v3.AuthConstructor):
    _auth_method_class = OAuth2Method
