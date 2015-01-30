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

from keystoneclient import base
from keystoneclient import exceptions
from keystoneclient.v3.contrib.user_registration.utils import REGISTRATION_PATH

class Token(base.Resource):
    pass

class TokenManager(base.CrudManager):
    """Manager class for manipulating passwords and tokens in
       the USER REGISTRATION extension for Keystone.

        For more information about the extension: https://www.github.com/ging/keystone
    """
    resource_class = Token
    collection_key = 'reset_password'
    key = 'reset_token'
    base_url = REGISTRATION_PATH

    def get_reset_token(self, user):
        base_url = self.base_url + '/users/{0}'.format(base.getid(user))
        return super(TokenManager, self).get(base_url=base_url)

    
