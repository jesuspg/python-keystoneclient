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
from keystoneclient import exceptions
from keystoneclient.v3.contrib.fiware_roles.utils import ROLES_PATH


class Role(base.Resource):
    pass

class RoleManager(base.CrudManager):
    """Manager class for manipulating roles in the FIWARE ROLES extension for Keystone.

        For more information about the extension: https://www.github.com/ging/keystone
    """
    resource_class = Role
    collection_key = 'roles'
    key = 'role'
    base_url = ROLES_PATH

    def _require_user_and_organization(self, user, organization):
        if (not user and organization) or (user and not organization):
            msg = 'Specify both a user and an organization'
            raise exceptions.ValidationError(msg)

    # def _require_user_xor_permission(self, user, permission):
    #     if user and permission:
    #         msg = 'Specify either a user or permission, not both'
    #         raise exceptions.ValidationError(msg)
    #     elif not (user or permission):
    #         msg = 'Must specify either a user or permission'
    #         raise exceptions.ValidationError(msg)

    def create(self, name, is_editable=True, application=None, **kwargs):
        return super(RoleManager, self).create(
                                        name=name,
                                        is_editable=is_editable,
                                        application=application,
                                        **kwargs)
    def get(self, role):
        return super(RoleManager, self).get(
                                    role_id=base.getid(role))

    def update(self, role, name=None, is_editable=True, 
                application=None, **kwargs):
        return super(RoleManager, self).update(
                                        role_id=base.getid(role),
                                        name=name,
                                        is_editable=is_editable,
                                        application=application,
                                        **kwargs)
        
    def delete(self, role):
        return super(RoleManager, self).delete(role_id=base.getid(role))

    def list(self, user=None, organization=None, **kwargs):
        self._require_user_and_organization(user, organization)

        if user and organization:
            base_url = self.base_url + '/users/%s/organizations/%s' \
                % (base.getid(user), base.getid(organization))
        else:
            base_url = self.base_url

        return super(RoleManager, self).list(base_url=base_url, **kwargs)

    def add_to_user(self, role, user, organization):
        base_url = self.base_url + '/users/%s/organizations/%s' \
            % (base.getid(user), base.getid(organization))
        
        return super(RoleManager, self).put(
                base_url=base_url,
                role_id=base.getid(role))

    def remove_from_user(self, role, user, organization):
        base_url = self.base_url + '/users/%s/organizations/%s' \
            % (base.getid(user), base.getid(organization))
    
        return super(RoleManager, self).delete(
                base_url=base_url,
                role_id=base.getid(role))

    def list_allowed_roles_to_assign(self, user, organization):
        """Obtain a list of all the roles the user is allowed to assign
        for every application.
        """
        endpoint = self.base_url + '/users/%s/organizations/%s/roles/allowed' \
            % (base.getid(user), base.getid(organization))
        resp, body = self.client.get(endpoint)
        allowed_roles = json.loads(resp.content)
        roles_as_resource = {}
        for app in allowed_roles:
            for role in allowed_roles[app]:
                roles_as_resource[app] = roles_as_resource.get(app, [])
                roles_as_resource[app].append(self.resource_class(self, role))
        return roles_as_resource

    