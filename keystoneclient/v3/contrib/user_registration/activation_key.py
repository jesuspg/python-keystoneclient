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

class ActivationKey(base.Resource):
    pass

class ActivationKeyManager(base.CrudManager):
    """Manager class for activating user in the USER REGISTRATION extension for Keystone.

        For more information about the extension: https://www.github.com/ging/keystone
    """
    resource_class = ActivationKey
    collection_key = 'activate'
    key = 'activation_key'
    base_url = REGISTRATION_PATH

    def new_activation_key(self, user):
        base_url = self.base_url + '/users/{0}'.format(base.getid(user))
        return super(ActivationKeyManager, self).get(base_url=base_url)

    