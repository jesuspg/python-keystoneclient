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

class Users(base.Resource):
    pass

class UsersManager(base.CrudManager):
    """Manager class for manipulating user registration in the USER REGISTRATION
        extension for Keystone.
        For more information about the extension: https://www.github.com/ging/keystone
    """
    resource_class = Users
    collection_key = 'users'
    key = 'user'
    base_url = REGISTRATION_PATH


    def register_user(self, name, domain=None, password=None,
                      username=None, description=None, **kwargs):

        user_data = base.filter_none(name=name,
                                     domain_id=base.getid(domain),
                                     password=password,
                                     username=username,
                                     description=description,
                                     **kwargs)

        return self._create(self.base_url+'/users', {'user': user_data}, 'user',
                            log=not bool(password))

    def activate_user(self, user, activation_key):
        url = self.base_url + '/activate/{0}/users/{1}'.format(
                                                base.getid(activation_key),
                                                base.getid(user))
        return self._update(
            url,
            None,
            self.key,
            method='PATCH')

    def reset_password(self, user, reset_token, new_password):
        url = self.base_url + '/reset_password/{0}/users/{1}'.format(
            base.getid(reset_token), base.getid(user))
        body = {
            'user' : {
                'password' : new_password,
            }
        }
        return self._update(
            url,
            body=body,
            response_key=self.key,
            method='PATCH')