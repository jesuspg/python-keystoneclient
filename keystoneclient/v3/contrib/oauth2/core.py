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

from keystoneclient.v3.contrib.oauth2 import access_tokens
from keystoneclient.v3.contrib.oauth2 import authorization_codes
from keystoneclient.v3.contrib.oauth2 import consumers


def create_oauth_manager(self):
        # TODO(garcianavalon) this is no longer necesary, remove
        return OAuthManager(self)

class OAuthManager(object):
    def __init__(self, api):
        self.access_tokens = access_tokens.AccessTokenManager(api)
        self.consumers = consumers.ConsumerManager(api)
        self.authorization_codes = authorization_codes.AuthorizationCodeManager(api)