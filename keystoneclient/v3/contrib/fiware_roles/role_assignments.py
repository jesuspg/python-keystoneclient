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

#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from keystoneclient import base
from keystoneclient import exceptions
from keystoneclient.v3.contrib.fiware_roles.utils import ROLES_PATH

class RoleAssignment(base.Resource):
    pass


class RoleAssignmentManager(base.CrudManager):

    """Manager class for manipulating user and organization roles assignments."""
    resource_class = RoleAssignment
    collection_key = 'role_assignments'
    key = 'role_assignment'
    base_url = ROLES_PATH

    def list_user_role_assignments(self, user=None, organization=None, 
    							   application=None, default_organization=False):
        """Lists role assignments for users.

        If no arguments are provided, all role assignments in the
        system will be listed.

        :param user: User to be used as query filter. (optional)
        :param organization: Project to be used as query filter.
                        (optional)
        :param application: Application to be used as query
                       filter. (optional)
        :param default_organization: If set to true, the endpoint will filter role assignments
            only in the default_project_id and the organization param is ignored. (optional)
        """

        query_params = {}
        if user:
            query_params['user_id'] = base.getid(user)
        if organization:
            query_params['organization_id'] = base.getid(organization)
        if application:
            query_params['application_id'] = base.getid(application)
        if default_organization:
            query_params['default_organization'] = True

        base_url = self.base_url + '/users'
        return super(RoleAssignmentManager, self).list(base_url=base_url, 
        											   **query_params)

    def list_organization_role_assignments(self, organization=None, 
    							   		   application=None):
        """Lists role assignments for organizations.

        If no arguments are provided, all role assignments in the
        system will be listed.

        :param organization: Project to be used as query filter.
                        (optional)
        :param application: Domain to be used as query
                       filter. (optional)
        """

        query_params = {}
        if organization:
            query_params['organization_id'] = base.getid(organization)
        if application:
            query_params['application_id'] = base.getid(application)

        base_url = self.base_url + '/organizations'
        return super(RoleAssignmentManager, self).list(base_url=base_url, 
        											   **query_params)

    def create(self, **kwargs):
        raise exceptions.MethodNotImplemented('Create not supported for'
                                              ' role assignments')

    def update(self, **kwargs):
        raise exceptions.MethodNotImplemented('Update not supported for'
                                              ' role assignments')

    def get(self, **kwargs):
        raise exceptions.MethodNotImplemented('Get not supported for'
                                              ' role assignments')

    def find(self, **kwargs):
        raise exceptions.MethodNotImplemented('Find not supported for'
                                              ' role assignments')

    def put(self, **kwargs):
        raise exceptions.MethodNotImplemented('Put not supported for'
                                              ' role assignments')

    def delete(self, **kwargs):
        raise exceptions.MethodNotImplemented('Delete not supported for'
                                              ' role assignments')
