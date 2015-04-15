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

import uuid

from keystoneclient.tests.unit.v3 import utils
from keystoneclient.v3.contrib.user_registration import users
from keystoneclient.v3.contrib.user_registration import activation_key
from keystoneclient.v3.contrib.user_registration import token


EXTENSION_PATH = 'OS-REGISTRATION'

class UsersTests(utils.TestCase):

    def setUp(self):
        super(UsersTests, self).setUp()
        self.key = 'user'
        self.collection_key = 'users'
        self.model = users.Users
        self.manager = self.client.user_registration.users
        self.path_prefix = EXTENSION_PATH


    def test_register_user(self):
        name = uuid.uuid4().hex
        user_ref = {
            'user': {
                'id': uuid.uuid4().hex,
                'name': name,
                'activation_key': uuid.uuid4().hex,
            }
        }
        self.stub_url('POST',
                      [self.path_prefix, self.collection_key],
                      json=user_ref,
                      status_code=201)

        self.manager.register_user(name=name)

    def test_activate_user(self):
        user_id = uuid.uuid4().hex
        activation_key = uuid.uuid4().hex
        self.stub_url('PATCH',
                      [self.path_prefix, 'activate', activation_key,
                       'users', user_id],
                      status_code=200)
        self.manager.activate_user(user=user_id, activation_key=activation_key)

    def test_reset_password(self):
        user_id = uuid.uuid4().hex
        token = uuid.uuid4().hex
        password = uuid.uuid4().hex
        self.stub_url('PATCH',
                      [self.path_prefix, 'reset_password', token,
                       self.collection_key, user_id],
                      status_code=204)
        self.manager.reset_password(user=user_id, 
                                    reset_token=token, 
                                    new_password=password)

class ActivationKeyTests(utils.TestCase):

    def setUp(self):
        super(ActivationKeyTests, self).setUp()
        self.key = 'activation_key'
        self.collection_key = 'activate'
        self.model = activation_key.ActivationKey
        self.manager = self.client.user_registration.activation_key
        self.path_prefix = EXTENSION_PATH

    def test_new_activation_key(self):
        user_id = uuid.uuid4().hex
        activation_key_ref = {
            'activation_key': {
                'id': uuid.uuid4().hex
            }
        }
        self.stub_url('GET',
                      [self.path_prefix, 'users',
                       user_id, 'activate'],
                      json=activation_key_ref,
                      status_code=200)
        self.manager.new_activation_key(user=user_id)

class TokenTest(utils.TestCase):

    def setUp(self):
        super(TokenTest, self).setUp()
        self.key = 'token'
        self.collection_key = 'reset_password'
        self.model = token.Token
        self.manager = self.client.user_registration.token
        self.path_prefix = EXTENSION_PATH

    def test_get_reset_token(self):
        user_id = uuid.uuid4().hex
        reset_token_ref = {
            'reset_token': {
                'id': uuid.uuid4().hex
            }
        }
        self.stub_url('GET',
                      [self.path_prefix, 'users',
                       user_id, self.collection_key],
                       json=reset_token_ref,
                      status_code=204)
        self.manager.get_reset_token(user=user_id)
