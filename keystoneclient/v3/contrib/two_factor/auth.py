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


import copy

from oslo_config import cfg

from keystoneclient.auth.identity import v3


class TwoFactorMethod(v3.PasswordMethod):
    """Construct a User/Password based authentication method with an extra verification code.

    :param string password: Password for authentication.
    :param string username: Username for authentication.
    :param string user_id: User ID for authentication.
    :param string user_domain_id: User's domain ID for authentication.
    :param string user_domain_name: User's domain name for authentication.
    :param string verification_code: Code generated through the key and the timestamp.
    :param dict device_data: Info from the client cookie to bypass verification code.
    """

    _method_parameters = [
        'user_id',
        'username',
        'user_domain_id',
        'user_domain_name',
        'password',
        'verification_code'
    ]


    def get_auth_data(self, session, auth, headers, **kwargs):
        method, payload = super(TwoFactorMethod, self).get_auth_data(session, auth, headers, **kwargs)

        if self.verification_code:
            payload['user']['verification_code'] = self.verification_code

        return method, payload


class TwoFactor(v3.Password):
    """AuthPlugin for TwoFactorMethod."""
    _auth_method_class = TwoFactorMethod

    @classmethod
    def get_options(cls):
        options = super(TwoFactor, cls).get_options()

        options.extend([
            cfg.StrOpt('verification-code', help='Generated code by timestamp')
        ])

        return options