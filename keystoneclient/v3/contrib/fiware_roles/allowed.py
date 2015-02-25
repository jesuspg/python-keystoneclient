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

from keystoneclient import base
from keystoneclient.v3.contrib.fiware_roles.utils import ROLES_PATH



class AllowedManager(base.Manager):
    """Manager class for obtaining allowed items based on internal permissions
    in the FIWARE ROLES extension for Keystone.

    For more information about the extension: https://www.github.com/ging/keystone
    """
    base_url = ROLES_PATH

    def list_user_allowed_roles_to_assign(self, user, organization):
        """Obtain a list of all the roles the user is allowed to assign
        for every application.
        """
        endpoint = (self.base_url + '/users/{0}/organizations/{1}/roles/allowed'
            ).format(base.getid(user), base.getid(organization))
        resp, body = self.client.get(endpoint)
        allowed_roles = json.loads(resp.content)['allowed_roles']
        return allowed_roles

    def list_organization_allowed_roles_to_assign(self, organization):
        """Obtain a list of all the roles the user is allowed to assign
        for every application.
        """
        endpoint = self.base_url + '/organizations/{0}/roles/allowed'.format(
            base.getid(organization))
        resp, body = self.client.get(endpoint)
        allowed_roles = json.loads(resp.content)['allowed_roles']
        return allowed_roles
    
    def list_user_allowed_applications_to_manage(self, user, organization):
        """Obtain a list of all the applications the user is allowed to manage.
        """
        endpoint = (self.base_url + '/users/{0}/organizations/{1}/applications/allowed'
            ).format(base.getid(user), base.getid(organization))
        resp, body = self.client.get(endpoint)
        allowed_applications = json.loads(resp.content)['allowed_applications']
        return allowed_applications

    def list_organization_allowed_applications_to_manage(self, organization):
        """Obtain a list of all the applications the user is allowed to manage.
        """
        endpoint = self.base_url + '/organizations/{0}/applications/allowed'.format(
            base.getid(organization))
        resp, body = self.client.get(endpoint)
        allowed_applications = json.loads(resp.content)['allowed_applications']
        return allowed_applications

    def list_user_allowed_applications_to_manage_roles(self, user, organization):
        """Obtain a list of all the applications the user is allowed to manage.
        """
        endpoint = (self.base_url + '/users/{0}/organizations/{1}/applications/allowed_roles'
            ).format(base.getid(user), base.getid(organization))
        resp, body = self.client.get(endpoint)
        allowed_applications = json.loads(resp.content)['allowed_applications']
        return allowed_applications

    def list_organization_allowed_applications_to_manage_roles(self, organization):
        """Obtain a list of all the applications the user is allowed to manage.
        """
        endpoint = self.base_url + '/organizations/{0}/applications/allowed_roles'.format(
            base.getid(organization))
        resp, body = self.client.get(endpoint)
        allowed_applications = json.loads(resp.content)['allowed_applications']
        return allowed_applications