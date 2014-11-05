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
from keystoneclient.v3.contrib.fiware_roles.utils import ROLES_PATH

class Permission(base.Resource):
    pass
    
class PermissionManager(base.CrudManager):
    """Manager class for manipulating permissions in the FIWARE ROLES extension for Keystone.

        For more information about the extension: https://www.github.com/ging/keystone
    """
    resource_class = Permission
    collection_key = 'permissions'
    key = 'permission'
    base_url = ROLES_PATH
