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

from keystoneclient.v3.contrib.user_registration import users, activation_key, token

class UserRegistrationManager(object):
    def __init__(self, api):
        self.users = users.UsersManager(api)
        self.activation_key = activation_key.ActivationKeyManager(api)
        self.token = token.TokenManager(api)
