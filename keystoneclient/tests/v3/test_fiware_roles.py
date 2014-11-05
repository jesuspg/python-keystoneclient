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

import uuid

from keystoneclient import exceptions
from keystoneclient.tests.v3 import utils
from keystoneclient.v3.contrib.fiware_roles import roles
from keystoneclient.v3.contrib.fiware_roles import permissions

EXTENSION_PATH = 'OS-ROLES'

class RoleTests(utils.TestCase, utils.CrudTests):


    def setUp(self):
        super(RoleTests, self).setUp()
        self.key = 'role'
        self.collection_key = 'roles'
        self.model = roles.Role
        self.manager = self.client.fiware_roles.roles
        self.path_prefix = EXTENSION_PATH

    def new_ref(self, **kwargs):
        kwargs = super(RoleTests, self).new_ref(**kwargs)
        kwargs.setdefault('name', uuid.uuid4().hex)
        kwargs.setdefault('is_editable', True)
        return kwargs

    def test_add_permission_to_role(self):

        permission_id = uuid.uuid4().hex
        role_ref = self.new_ref()
        self.stub_url('PUT',
                      [self.path_prefix, self.collection_key, role_ref['id'], 
                        'permissions', permission_id],
                      status_code=204)
        self.manager.add_permission(role=role_ref['id'], permission=permission_id)

        # Test invalid args
        self.assertRaises(exceptions.ValidationError,
                          self.manager.add_permission,
                          role=role_ref['id'],
                          permission=None)
        self.assertRaises(exceptions.ValidationError,
                          self.manager.add_permission,
                          role=None,
                          permission=permission_id)

class PermissionTests(utils.TestCase, utils.CrudTests):


    def setUp(self):
        super(PermissionTests, self).setUp()
        self.key = 'permission'
        self.collection_key = 'permissions'
        self.model = permissions.Permission
        self.manager = self.client.fiware_roles.permissions
        self.path_prefix = EXTENSION_PATH

    def new_ref(self, **kwargs):
        kwargs = super(PermissionTests, self).new_ref(**kwargs)
        kwargs.setdefault('name', uuid.uuid4().hex)
        kwargs.setdefault('is_editable', True)
        return kwargs