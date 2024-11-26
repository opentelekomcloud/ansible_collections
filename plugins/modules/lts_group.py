#!/usr/bin/python
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

DOCUMENTATION = '''
module: lts_group
short_description: Manage LTS loggroup on Open Telekom Cloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.1.x"
author: "Daniela Ebert"
description:
  - Manage LTS loggroup on Open Telekom Cloud
options:
  name:
    description:
      - Name of the log group to be created
    type: str
    required: true
  ttl_in_days:
    description:
      - Log retention duration, default 7 days
    type: int
    required: true
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
log_group_id:
    description: ID of the newly created log group
    type: str
    sample: {
        {
        "loggroup_id": "xxxxxxxx-8165-449a-9e7e-xxxxxxxxxxxx"
        }
    }
'''

EXAMPLES = '''
# Create LTS log group
- opentelekomcloud.cloud.lts_group:
    name: 'lts-test'
    ttl_in_days: '7'
# Delete LTS log group
- opentelekomcloud.cloud.lts_group:
    name: 'lts-test'
    state: absent
# Update LTS log group
- opentelekomcloud.cloud.lts_group:
    name: 'lts-test'
    ttl_in_days: 3
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class LtsGroupModule(OTCModule):
    argument_spec = dict(
        name=dict(required=True),
        ttl_in_days=dict(required=False, default='7'),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        attrs = {}
        group = ""
        group_list = []
        groupid_list = []

        # Get existing log groups with id's
        for x in self.conn.lts.groups():
            group_list.append(x.name)
            groupid_list.append(x.id)

        # Check if log group exists, get id
        attrs['name'] = self.params['name']
        if attrs['name'] in group_list:
            group = attrs['name']
            i = group_list.index(group)
            groupid = groupid_list[i]

        if self.params['ttl_in_days']:
            attrs['ttl_in_days'] = self.params['ttl_in_days']

        if self.params['state'] == 'present':

            # Instance creation
            if not group:
                if self.ansible.check_mode:
                    self.exit(changed=True)
                group = self.conn.lts.create_group(**attrs)
                self.exit(changed=True, group=group.to_dict())

            # Instance Modification
            elif group:
                if self.params['ttl_in_days']:
                    attrs['ttl_in_days'] = self.params['ttl_in_days']

                if self.ansible.check_mode:
                    self.exit(changed=True)
                group = self.conn.lts.update_group(group=groupid, **attrs)
                self.exit(changed=True, group=group.to_dict())

        if self.params['state'] == 'absent':

            # Instance Deletion
            if group:
                if self.ansible.check_mode:
                    self.exit(changed=True)
                group = self.conn.lts.delete_group(group=groupid)
                self.exit(changed=True, group=group)

            elif not group:
                self.exit(
                    changed=False,
                    failed=True,
                    message=('No Group with name %s found') % (self.params['name'])
                )


def main():
    module = LtsGroupModule()
    module()


if __name__ == "__main__":
    main()
