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

from keystoneclient.tests.unit.v3 import utils
from keystoneclient.v3.contrib import endpoint_filter


EXTENSION_PATH = 'OS-EP-FILTER'

class EndpointGroupsFiltersTests(utils.TestCase, utils.CrudTests):


    def setUp(self):
        super(EndpointGroupsFiltersTests, self).setUp()
        self.key = 'endpoint_group'
        self.collection_key = 'endpoint_groups'
        self.model = endpoint_filter.EndpointGroupFilter
        self.manager = self.client.endpoint_groups
        self.path_prefix = EXTENSION_PATH

    def new_ref(self, **kwargs):
        kwargs = super(EndpointGroupsFiltersTests, self).new_ref(**kwargs)
        kwargs.setdefault('name', uuid.uuid4().hex)
        kwargs.setdefault('description', uuid.uuid4().hex)
        kwargs.setdefault('filters', {})
        return kwargs