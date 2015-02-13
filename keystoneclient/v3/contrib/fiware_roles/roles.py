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

    def create(self, name, is_internal=False, application=None, **kwargs):
        return super(RoleManager, self).create(
            name=name,
            is_internal=is_internal,
            application=base.getid(application),
            **kwargs)
    

    def get(self, role):
        return super(RoleManager, self).get(role_id=base.getid(role))


    def update(self, role, name=None, is_internal=False, 
               application=None, **kwargs):
        return super(RoleManager, self).update(role_id=base.getid(role),
                                               name=name,
                                               is_internal=is_internal,
                                               application=base.getid(application),
                                               **kwargs)
   

    def delete(self, role):
        return super(RoleManager, self).delete(role_id=base.getid(role))


    def list(self, **kwargs):
        base_url = self.base_url
        return super(RoleManager, self).list(base_url=base_url, **kwargs)


    # ROLE-USER
    def add_to_user(self, role, user, organization, application):
        base_url = (self.base_url + '/users/{0}/organizations/{1}/applications/{2}'
            ).format(base.getid(user), base.getid(organization), 
            base.getid(application))
        
        return super(RoleManager, self).put(base_url=base_url,
                                            role_id=base.getid(role))


    def remove_from_user(self, role, user, organization, application):
        base_url = (self.base_url + '/users/{0}/organizations/{1}/applications/{2}'
            ).format(base.getid(user), base.getid(organization), 
            base.getid(application))
    
        return super(RoleManager, self).delete(base_url=base_url,
                                               role_id=base.getid(role))


    def list_user_allowed_roles_to_assign(self, user, organization):
        """Obtain a list of all the roles the user is allowed to assign
        for every application.
        """
        endpoint = (self.base_url + '/users/{0}/organizations/{1}/roles/allowed'
            ).format(base.getid(user), base.getid(organization))
        resp, body = self.client.get(endpoint)
        allowed_roles = json.loads(resp.content)['allowed_roles']
        return allowed_roles
        # roles_as_resource = {}
        # for app in allowed_roles:
        #     for role in allowed_roles[app]:
        #         roles_as_resource[app] = roles_as_resource.get(app, [])
        #         roles_as_resource[app].append(self.resource_class(self, role))
        # return roles_as_resource


    # ROLES-ORGANIZATIONS
    def add_to_organization(self, role, organization, application):
        base_url = (self.base_url + '/organizations/{0}/applications/{1}'
            ).format(base.getid(organization), base.getid(application))
        
        return super(RoleManager, self).put(base_url=base_url,
                                            role_id=base.getid(role))


    def remove_from_organization(self, role, organization, application):
        base_url = (self.base_url + '/organizations/{0}/applications/{1}'
            ).format(base.getid(organization), base.getid(application))
        return super(RoleManager, self).delete(base_url=base_url,
                                               role_id=base.getid(role))


    def list_organization_allowed_roles_to_assign(self, organization):
        """Obtain a list of all the roles the user is allowed to assign
        for every application.
        """
        endpoint = self.base_url + '/organizations/{0}/roles/allowed'.format(
            base.getid(organization))
        resp, body = self.client.get(endpoint)
        allowed_roles = json.loads(resp.content)['allowed_roles']
        return allowed_roles
        # roles_as_resource = {}
        # for app in allowed_roles:
        #     for role in allowed_roles[app]:
        #         roles_as_resource[app] = roles_as_resource.get(app, [])
        #         roles_as_resource[app].append(self.resource_class(self, role))
        # return roles_as_resource

    