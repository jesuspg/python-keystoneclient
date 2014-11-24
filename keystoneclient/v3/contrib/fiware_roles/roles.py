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

    def _require_role_and_user_and_organization(self, role, user, organization):
        if not(role and user and organization):
            msg = 'Specify a role, a user and an organization'
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

    def list(self, user=None, **kwargs):
    # def list(self, user=None, permission=None, **kwargs):    
        # if user or permission:
        #     self._require_user_xor_permission(user, permission)

        if user:
            base_url = self.base_url + '/users/%s' % base.getid(user)

        # elif permission:
        #     base_url = self.base_url +  '/permissions/%s' % base.getid(permission)

        else:
            base_url = self.base_url

        return super(RoleManager, self).list(base_url=base_url, **kwargs)


    def add_to_user(self, role, user, organization):
        self._require_role_and_user_and_organization(role, user, organization)
        base_url = self.base_url + '/users/%s/organizations/%s' % (base.getid(user), base.getid(organization))
        
        return super(RoleManager, self).put(
                base_url=base_url,
                role_id=base.getid(role))

    def remove_from_user(self, role, user, organization):
        self._require_role_and_user_and_organization(role, user, organization)
        base_url = self.base_url + '/users/%s/organizations/%s' % (base.getid(user), base.getid(organization))
    
        return super(RoleManager, self).delete(
                base_url=base_url,
                role_id=base.getid(role))


    