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

import logging

from keystoneclient import base
from keystoneclient import exceptions

from keystoneclient.v3.contrib.fiware_roles import core


LOG = logging.getLogger(__name__)

class Role(base.Resource):
    pass

class RoleManager(base.CrudManager):
    """Manager class for manipulating roles in the FIWARE ROLES extension for Keystone.

        For more information about the extension: https://www.github.com/ging/keystone
    """
    resource_class = Role
    collection_key = 'roles'
    key = 'role'
    base_url = core.ROLES_PATH

    def _require_role_and_permission(self, role, permission):
        if not (role and permission):
            msg = 'Specify both a role and a permission'
            raise exceptions.ValidationError(msg)

    def add_permission(self, role, permission):
        self._require_role_and_permission(role, permission)
        
        # PUT to roles/{role_id}/permissions
        base_url = self.base_url + '%s/permissions/' %base.getid(role)
        return super(RoleManager, self).put(
            base_url=base_url,
            permission_id=base.getid(permission))

