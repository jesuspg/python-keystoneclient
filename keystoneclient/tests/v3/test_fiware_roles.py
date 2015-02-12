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
from keystoneclient.v3.contrib.fiware_roles import role_assignments
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
        kwargs.setdefault('is_internal', False)
        return kwargs

    # ROLES-USER
    def test_add_role_to_user(self):
        user_id = uuid.uuid4().hex
        role_ref = self.new_ref()
        organization_id = uuid.uuid4().hex
        app_id = uuid.uuid4().hex
        self.stub_url('PUT',
                      [self.path_prefix, 'users', user_id,
                      'organizations', organization_id,
                      'applications', app_id,
                       self.collection_key, role_ref['id']],
                       status_code=204)
        self.manager.add_to_user(role=role_ref['id'], 
                              user=user_id,
                              organization=organization_id,
                              application=app_id)


    def test_remove_role_from_user(self):
        user_id = uuid.uuid4().hex
        role_ref = self.new_ref()
        organization_id = uuid.uuid4().hex
        app_id = uuid.uuid4().hex
        self.stub_url('DELETE',
                      [self.path_prefix, 'users', user_id,
                       'organizations', organization_id,
                       'applications', app_id,
                        self.collection_key, role_ref['id']],
                      status_code=204)

        self.manager.remove_from_user(role=role_ref['id'], 
                                 user=user_id,
                                 organization=organization_id,
                                 application=app_id)


    def test_list_user_allowed_roles_to_assign(self):
      user_id = uuid.uuid4().hex
      organization_id = uuid.uuid4().hex
      allowed_roles_ref = {
        'some_application': [
            self.new_ref(),
            self.new_ref(),
        ]
      }
      self.stub_url('GET',
                      [self.path_prefix, 'users', user_id,
                            'organizations', organization_id,
                            'roles/allowed'],
                      json=allowed_roles_ref)
      allowed_roles = self.manager.list_user_allowed_roles_to_assign(
        user=user_id, organization=organization_id)

      self.assertIsNotNone(allowed_roles)
      for item in allowed_roles['some_application']:
        self.assertIsInstance(item, self.model)


    # ROLES-ORGANIZATIONS
    def test_add_role_to_organization(self):
        organization_id = uuid.uuid4().hex
        role_ref = self.new_ref()
        app_id = uuid.uuid4().hex
        self.stub_url('PUT',
                      [self.path_prefix, 'organizations', organization_id,
                      'applications', app_id,
                      self.collection_key, role_ref['id']],
                      status_code=204)
        self.manager.add_to_organization(role=role_ref['id'], 
                                         organization=organization_id,
                                         application=app_id)


    def test_remove_role_from_organization(self):
        organization_id = uuid.uuid4().hex
        role_ref = self.new_ref()
        app_id = uuid.uuid4().hex
        self.stub_url('DELETE',
                      [self.path_prefix, 'organizations', organization_id,
                      'applications', app_id,
                      self.collection_key, role_ref['id']],
                      status_code=204)

        self.manager.remove_from_organization(role=role_ref['id'], 
                                              organization=organization_id,
                                              application=app_id)


    def test_list_organization_allowed_roles_to_assign(self):
      organization_id = uuid.uuid4().hex
      allowed_roles_ref = {
        'some_application': [
            self.new_ref(),
            self.new_ref(),
        ]
      }
      self.stub_url('GET',
                    [self.path_prefix, 'organizations', organization_id,
                    'roles/allowed'],
                    json=allowed_roles_ref)
      allowed_roles = self.manager.list_organization_allowed_roles_to_assign(
        organization=organization_id)

      self.assertIsNotNone(allowed_roles)
      for item in allowed_roles['some_application']:
        self.assertIsInstance(item, self.model)



class RoleAssignmentsTests(utils.TestCase, utils.CrudTests):

    def setUp(self):
        super(RoleAssignmentsTests, self).setUp()
        self.key = 'role_assignment'
        self.collection_key = 'role_assignments'
        self.model = role_assignments.RoleAssignment
        self.manager = self.client.fiware_roles.role_assignments
        self.USER_ASSIGNMENT_TEST_LIST = [{
            'role_id': uuid.uuid4().hex,
            'organization_id': uuid.uuid4().hex,
            'user_id': uuid.uuid4().hex,
            'application_id': uuid.uuid4().hex,
        }]
        self.ORGANIZATION_ASSIGNMENT_TEST_LIST = [{
            'role_id': uuid.uuid4().hex,
            'organization_id': uuid.uuid4().hex,
            'application_id': uuid.uuid4().hex,
        }]
        self.path_prefix = EXTENSION_PATH


    def _assert_returned_list(self, ref_list, returned_list):
        self.assertEqual(len(ref_list), len(returned_list))
        [self.assertIsInstance(r, self.model) for r in returned_list]


    # ROLE-USER
    def test_all_user_assignments_list(self):
        ref_list = self.USER_ASSIGNMENT_TEST_LIST
        self.stub_entity('GET',
                         [self.path_prefix, 'users', self.collection_key],
                         entity=ref_list)

        returned_list = self.manager.list_user_role_assignments()
        self._assert_returned_list(ref_list, returned_list)

        kwargs = {}
        self.assertQueryStringContains(**kwargs)


    def test_filter_by_organization_user_assignments(self):
        ref_list = self.USER_ASSIGNMENT_TEST_LIST
        self.stub_entity('GET',
                         [self.path_prefix, 'users', self.collection_key,
                          '?organization_id=%s' % self.TEST_TENANT_ID],
                         entity=ref_list)

        returned_list = self.manager.list_user_role_assignments(
            organization=self.TEST_TENANT_ID)
        self._assert_returned_list(ref_list, returned_list)

        kwargs = {'organization_id': self.TEST_TENANT_ID}
        self.assertQueryStringContains(**kwargs)


    def test_filter_by_application_user_assignments(self):
        ref_list = self.USER_ASSIGNMENT_TEST_LIST
        self.stub_entity('GET',
                         [self.path_prefix, 'users', self.collection_key,
                          '?application_id=%s' % self.TEST_DOMAIN_ID],
                         entity=ref_list)

        returned_list = self.manager.list_user_role_assignments(
            application=self.TEST_DOMAIN_ID)
        self._assert_returned_list(ref_list, returned_list)

        kwargs = {'application_id': self.TEST_DOMAIN_ID}
        self.assertQueryStringContains(**kwargs)


    def test_filter_by_user_user_assignments(self):
        ref_list = self.USER_ASSIGNMENT_TEST_LIST
        self.stub_entity('GET',
                         [self.path_prefix, 'users', self.collection_key,
                          '?user_id=%s' % self.TEST_USER_ID],
                         entity=ref_list)

        returned_list = self.manager.list_user_role_assignments(
            user=self.TEST_USER_ID)
        self._assert_returned_list(ref_list, returned_list)

        kwargs = {'user_id': self.TEST_USER_ID}
        self.assertQueryStringContains(**kwargs)


    def test_filter_by_user_and_organization_user_assignments(self):
        ref_list = self.USER_ASSIGNMENT_TEST_LIST
        self.stub_entity('GET',
                         [self.path_prefix, 'users', self.collection_key,
                          '?organization_id=%s&user_id=%s' %
                          (self.TEST_TENANT_ID, self.TEST_USER_ID)],
                         entity=ref_list)

        returned_list = self.manager.list_user_role_assignments(
            user=self.TEST_USER_ID, organization=self.TEST_TENANT_ID)
        self._assert_returned_list(ref_list, returned_list)

        kwargs = {'organization_id': self.TEST_TENANT_ID,
                  'user_id': self.TEST_USER_ID}
        self.assertQueryStringContains(**kwargs)


    #ROLE-ORGANIZATION
    def test_all_organization_assignments_list(self):
        ref_list = self.ORGANIZATION_ASSIGNMENT_TEST_LIST
        self.stub_entity('GET',
                         [self.path_prefix, 'organizations', self.collection_key],
                         entity=ref_list)

        returned_list = self.manager.list_organization_role_assignments()
        self._assert_returned_list(ref_list, returned_list)

        kwargs = {}
        self.assertQueryStringContains(**kwargs)


    def test_filter_by_organization_organization_assignments(self):
        ref_list = self.ORGANIZATION_ASSIGNMENT_TEST_LIST
        self.stub_entity('GET',
                         [self.path_prefix, 'organizations', self.collection_key,
                          '?organization_id=%s' % self.TEST_TENANT_ID],
                         entity=ref_list)

        returned_list = self.manager.list_organization_role_assignments(
            organization=self.TEST_TENANT_ID)
        self._assert_returned_list(ref_list, returned_list)

        kwargs = {'organization_id': self.TEST_TENANT_ID}
        self.assertQueryStringContains(**kwargs)


    def test_filter_by_application_organization_assignments(self):
        ref_list = self.ORGANIZATION_ASSIGNMENT_TEST_LIST
        self.stub_entity('GET',
                         [self.path_prefix, 'organizations', self.collection_key,
                          '?application_id=%s' % self.TEST_DOMAIN_ID],
                         entity=ref_list)

        returned_list = self.manager.list_organization_role_assignments(
            application=self.TEST_DOMAIN_ID)
        self._assert_returned_list(ref_list, returned_list)

        kwargs = {'application_id': self.TEST_DOMAIN_ID}
        self.assertQueryStringContains(**kwargs)


    def test_filter_by_application_and_organization_organization_assignments(self):
        ref_list = self.ORGANIZATION_ASSIGNMENT_TEST_LIST
        self.stub_entity('GET',
                         [self.path_prefix, 'organizations', self.collection_key,
                          '?organization_id=%s&application_id=%s' %
                          (self.TEST_TENANT_ID, self.TEST_DOMAIN_ID)],
                         entity=ref_list)

        returned_list = self.manager.list_organization_role_assignments(
            application=self.TEST_DOMAIN_ID, organization=self.TEST_TENANT_ID)
        self._assert_returned_list(ref_list, returned_list)

        kwargs = {'organization_id': self.TEST_TENANT_ID,
                  'application_id': self.TEST_DOMAIN_ID}
        self.assertQueryStringContains(**kwargs)


    def test_create(self):
        # Create not supported for role assignments
        self.assertRaises(exceptions.MethodNotImplemented, self.manager.create)

    def test_update(self):
        # Update not supported for role assignments
        self.assertRaises(exceptions.MethodNotImplemented, self.manager.update)

    def test_delete(self):
        # Delete not supported for role assignments
        self.assertRaises(exceptions.MethodNotImplemented, self.manager.delete)

    def test_get(self):
        # Get not supported for role assignments
        self.assertRaises(exceptions.MethodNotImplemented, self.manager.get)

    def test_find(self):
        # Find not supported for role assignments
        self.assertRaises(exceptions.MethodNotImplemented, self.manager.find)


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
        kwargs.setdefault('is_internal', False)
        return kwargs

    def test_list_permissions_by_role(self):
        role_id = uuid.uuid4().hex
        ref_list = [self.new_ref(), self.new_ref()]

        self.stub_entity('GET',
                      parts=[self.path_prefix, 'roles', role_id, self.collection_key],
                      entity=ref_list)

        returned_list = self.manager.list(role=role_id)

        self.assertEqual(len(ref_list), len(returned_list))
        for item in returned_list:
            self.assertIsInstance(item, self.model)

    def test_add_permission_to_role(self):

        permission_id = uuid.uuid4().hex
        role_ref = self.new_ref()
        self.stub_url('PUT',
                      [self.path_prefix, 'roles', role_ref['id'],
                       self.collection_key, permission_id], 
                      status_code=204)
        self.manager.add_to_role(role=role_ref['id'], permission=permission_id)

        # Test invalid args
        self.assertRaises(exceptions.ValidationError,
                          self.manager.add_to_role,
                          role=role_ref['id'],
                          permission=None)
        self.assertRaises(exceptions.ValidationError,
                          self.manager.add_to_role,
                          role=None,
                          permission=permission_id)

    def test_remove_permission_from_role(self):

        permission_id = uuid.uuid4().hex
        role_ref = self.new_ref()
        self.stub_url('DELETE',
                      [self.path_prefix, 'roles', role_ref['id'],
                       self.collection_key, permission_id], 
                      status_code=204)
        self.manager.remove_from_role(role=role_ref['id'], permission=permission_id)

        # Test invalid args
        self.assertRaises(exceptions.ValidationError,
                          self.manager.remove_from_role,
                          role=role_ref['id'],
                          permission=None)
        self.assertRaises(exceptions.ValidationError,
                          self.manager.remove_from_role,
                          role=None,
                          permission=permission_id)

