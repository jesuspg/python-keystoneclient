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

    def _require_role_and_permission(self, role, permission):
        if not (role and permission):
            msg = 'Specify both a role and a permission'
            raise exceptions.ValidationError(msg)

    @base.filter_kwargs
    def put(self, append_to_url='', **kwargs):
        """Override to append elements to the url"""
        url = self.build_url(dict_args_in_out=kwargs)
        if append_to_url:
            url += append_to_url

        return self._update(
                        url,
                     method='PUT')

    def add_permission(self, role, permission):
        self._require_role_and_permission(role, permission)
        
        # PUT to roles/{role_id}/permissions
        endpoint = '/permissions/%s' %base.getid(permission)
        return self.put(append_to_url=endpoint,
                    role_id=base.getid(role))

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
        return super(RoleManager, self).delete(
                            role_id=base.getid(role))