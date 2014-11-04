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

import json
import urllib
import six
from six.moves.urllib import parse as urlparse

from keystoneclient import base
from keystoneclient.v3.contrib.oauth2 import utils


class AuthorizationCode(base.Resource):
    """ TODO(garcianavalon)
    """
    pass


class AuthorizationCodeManager(base.CrudManager):
    """Manager class for manipulating identity OAuth authorization codes."""
    resource_class = AuthorizationCode
    collection_key = 'authorization_codes'
    key = 'authorization_code'
    base_url = utils.OAUTH2_PATH

    def authorize(self, consumer, scopes, redirect=False):
        """Authorize a Consumer for certain scopes, getting an authorization code.

        The way the provider (Keystone) will return the code is in the header, as an
        HTTP redirection: 
        'Location': 'https://foo.com/welcome_back?code=somerandomstring&state=xyz'

        Utilize Identity API operation:
        POST /OS-OAUTH2/authorize/

        :param user: the user granting authorization
        :param consumer: the client that will be authorized, and
            will exchange the authorization code for an access token.
        :param scopes: a list of scopes. They are provided by the consumer
            in the authorization request
        :param redirect: The Keystone OAuth2 extension returns an HTTP 302 to 
            comply with RFC 6749 but in general we dont want the redirect to happen 
            if we are using the keystoneclient.
        """
        endpoint = self.base_url + '/authorize'
        body = {
            'user_auth': {
                'client_id':base.getid(consumer),
                'scopes':scopes
            }
        }
        response, body = self.client.post(endpoint, body=body, redirect=redirect)

        redirect_uri = response.headers.get('Location')

        parsed = urlparse.urlparse(redirect_uri)
        query = dict(urlparse.parse_qsl(parsed.query))
        authorization_code = {
            'redirect_uri':redirect_uri,
            'code': query['code'],
            'state': query['state']
        }

        return self.resource_class(self, authorization_code)

    def request_authorization(self, consumer, redirect_uri, scope, state=None):
        """ Send the consumer credentials to the OAuth2 provider. 

        The user then will be asked to authorize the client for the requested scopes. In 
        the OAuth2 flow this happens when the client(consumer) redirects the resource 
        owner(user) through his user agent to the authorization server(provider). 
        Therefore, this call is done by the user but with the data provided by the 
        consumer.

        Utilize Identity API operation:
        GET /OS-OAUTH2/authorize/?client_id=&redirect_uri=&response_type=code&state=

        :param consumer: the consumer asking for authorization
        :param redirect_uri: The url the user will be redirected to. It must be
            registered in the server asociated with the requesting consumer.
        :param scope: list of strings with the requested scopes from the ones
            defined by the provider.
        :param state: Optional, a string for consumer use.
        """
        # Transform the array with the requested scopes into a list of 
        # space-delimited, case-sensitive strings as specified in RFC 6749
        # http://tools.ietf.org/html/rfc6749#section-3.3
        scope_string = ' '.join(scope)
        
        # NOTE(garcianavalon) we use a list of tuples to ensure param order
        # in the query string to be able to mock it during testing.
        credentials = [
            ('response_type', 'code'),
            ('client_id', base.getid(consumer)),
            ('redirect_uri', redirect_uri),
            ('scope', scope_string),
            ('state', state)
        ]
        query = urllib.urlencode(credentials)
        endpoint = self.base_url + '/authorize?%s' %query

        response, body = self.client.get(endpoint)
        # TODO(garcianavalon) figure out the return. Do we need a separated manager?
        return json.loads(response.content)
