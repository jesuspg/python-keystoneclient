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
from keystoneclient.v3.contrib.oauth2 import utils

LOG = logging.getLogger(__name__)

class Consumer(base.Resource):
    """Represents an OAuth2 consumer.
    Attributes:
    * id: a uuid that identifies the consumer
    * description: a short description of the consumer
    * secret: string used by consumers to sign certain requests
    * client_type: string OAuth2 client type. The extension defines which client types
    are accepted
    * redirect_uris: List of strings with valid urls. This are the only urls the
    consumer is allowed to redirect to
    * grant_type: string with OAuth2 grant type. The extension defines which
    ones are accepted
    * response_type: string with the response types associated with the grant. The
    extension handles assigning this value to the correspoding one for grant_type. See
    https://oauthlib.readthedocs.org/en/latest/oauth2/oauth2.html for more info
    * scopes: list of strings with the scopes the consumer is going to use. Defined
    at the extension
    """
    pass

class ConsumerManager(base.CrudManager):
    """Manager class for manipulating identity consumers."""
    resource_class = Consumer
    collection_key = 'consumers'
    key = 'consumer'
    base_url = utils.OAUTH2_PATH

    def create(self, name, description=None, client_type=None, redirect_uris=[],
                grant_type=None, scopes=[], **kwargs):
        return super(ConsumerManager, self).create(
                                name=name,
                                description=description,
                                client_type=client_type,
                                redirect_uris=redirect_uris,
                                grant_type=grant_type,
                                scopes=scopes,
                                **kwargs)

    def get(self, consumer):
        return super(ConsumerManager, self).get(
                                    consumer_id=base.getid(consumer))

    def update(self, consumer, name=None, description=None, client_type=None, 
                redirect_uris=[], grant_type=None, scopes=[], **kwargs):
        return super(ConsumerManager, self).update(
                                        consumer_id=base.getid(consumer),
                                        name=name,
                                        description=description,
                                        client_type=client_type,
                                        redirect_uris=redirect_uris,
                                        grant_type=grant_type,
                                        scopes=scopes,
                                        **kwargs)
        
    def delete(self, consumer):
        return super(ConsumerManager, self).delete(
                            consumer_id=base.getid(consumer))

    def list(self, user=None, **kwargs):  
        if user:
            base_url = '/users/{0}'.format(base.getid(user)) + self.base_url

        else:
            base_url = self.base_url 
        return super(ConsumerManager, self).list(base_url=base_url, **kwargs)