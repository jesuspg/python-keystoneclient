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

from keystoneclient import session
from keystoneclient.tests.unit.v3 import client_fixtures
from keystoneclient.tests.unit.v3 import utils
from keystoneclient.v3.contrib.two_factor import keys
from keystoneclient.v3.contrib.two_factor import auth


EXTENSION_PATH = 'OS-TWO-FACTOR'

class UsersTests(utils.TestCase):

    def setUp(self):
        super(UsersTests, self).setUp()
        self.model = keys.Key
        self.manager = self.client.two_factor.keys
        self.path_prefix = EXTENSION_PATH

    def test_generate_new_key(self):
        user_id = uuid.uuid4().hex
        key_ref = {
            'two_factor_auth_data': {
                'security_answer': 'Sample answer',
                'security_question': 'Sample question',
                'two_factor_key': uuid.uuid4().hex,
                'user_id': user_id,
            }
        }
        self.stub_url('POST',
                      ['users/', user_id, self.path_prefix, '/two_factor_auth'],
                      json=key_ref,
                      status_code=201)

        self.manager.generate_new_key(user=user_id,
                                      security_question='Sample question',
                                      security_answer='Sample answer')

    def test_deactivate_two_factor(self):
        user_id = uuid.uuid4().hex

        self.stub_url('DELETE',
                      ['users/', user_id, self.path_prefix, '/two_factor_auth'],
                      status_code=204)

        self.manager.deactivate_two_factor(user=user_id)

    def test_check_activated_two_factor(self):
        user_id = uuid.uuid4().hex

        self.stub_url('HEAD',
                      [self.path_prefix, '/two_factor_auth'],
                      status_code=204)

        self.manager.check_activated_two_factor(user=user_id)


class TwoFactorAuthTests(utils.TestCase):


    def test_two_factor_authenticate_success(self):
        verification_code = uuid.uuid4().hex
        password = uuid.uuid4().hex
        user_id = uuid.uuid4().hex

        # Just use an existing project scoped token and change
        # the methods to password, and add its section.
        token = client_fixtures.unscoped_token()

        token['methods'] = ["password"]
        token['password'] = {
            "verification_code": verification_code,
            'password': password
        }
        self.stub_auth(json=token)

        a = auth.TwoFactor(
            self.TEST_URL,
            verification_code=verification_code,
            password=password,
            user_id=user_id)
        s = session.Session(auth=a)
        t = s.get_token()
        self.assertEqual(self.TEST_TOKEN, t)

        TWO_FACTOR_REQUEST_BODY = {
            "auth": {
                "identity": {
                    "methods": ["password"],
                    "password": {
                        'user': {
                            "verification_code": verification_code,
                            'password': password,
                            'id': user_id
                        }
                    }
                }
            }
        }

        self.assertRequestBodyIs(json=TWO_FACTOR_REQUEST_BODY)

    def test_two_factor_authenticate_scoped_success(self):

        verification_code = uuid.uuid4().hex
        password = uuid.uuid4().hex
        user_id = uuid.uuid4().hex

        # Just use an existing project scoped token and change
        # the methods to password, and add its section.
        token = client_fixtures.project_scoped_token()
        token['methods'] = ["password"]
        token['password'] = {
            "verification_code": verification_code,
            'password': password
        }
        self.stub_auth(json=token)

        a = auth.TwoFactor(
            self.TEST_URL,
            verification_code=verification_code,
            password=password,
            user_id=user_id)
        s = session.Session(auth=a)
        t = s.get_token()
        self.assertEqual(self.TEST_TOKEN, t)

        TWO_FACTOR_REQUEST_BODY = {
            "auth": {
                "identity": {
                    "methods": ["password"],
                    "password": {
                        'user': {
                            'verification_code': verification_code,
                            'password': password,
                            'id': user_id
                        }
                    }
                }
            }
        }

        self.assertRequestBodyIs(json=TWO_FACTOR_REQUEST_BODY)
