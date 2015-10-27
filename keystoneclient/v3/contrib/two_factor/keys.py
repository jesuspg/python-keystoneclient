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
import logging

from keystoneclient import base


LOG = logging.getLogger(__name__)

EXTENSION_PATH = '/OS-TWO-FACTOR-AUTHENTICATION'

class Key(base.Resource):
    pass


class KeyManager(base.Manager):
    """Manager class for creating/deleting two factor keys."""

    resource_class = Key
    base_url = EXTENSION_PATH + '/user/{user_id}'

    def _url(self, user):
        return self.base_url.format(user_id=base.getid(user))

    def generate_new_key(self, user):
        
        return super(KeyManager, self)._put(url=self._url(user))

    
    def deactivate_two_factor(self, user):
        
        return super(KeyManager, self)._delete(url=self._url(user))

    def check_activated_two_factor(self, user):
        
        return super(KeyManager, self)._head(url=self._url(user))
