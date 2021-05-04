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
module: dms_queue_group
short_description: Manage DMS Queue-Groups on Open Telekom Cloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.1.2"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Manage DMS Queue-Groups on Open Telekom Cloud
options:
  queue_name:
    description:
      - Name of the Queue. Can also be ID.
    type: str
    required: true
  group_name:
    description:
      - Name of the Group.
    type: str
    required: true
  state:
    choices: [present, absent]
    default: present
    description: Instance state
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
deh_host:
    description: Dictionary of DMS Queue
    returned: changed
    type: dict
    sample: {
        "group": {
            "available_deadletters": null,
            "available_messages": null,
            "consumed_messages": null,
            "id": "g-8f271ad2-ec43-4d6f-b9f0-ff060b864f85",
            "location": {
                "cloud": "otc",
                "project": {
                    "domain_id": null,
                    "domain_name": null,
                    "id": "16d53a84a13b49529d2e2c3646691288",
                    "name": "eu-de"
                },
                "region_name": "eu-de",
                "zone": null
            },
            "name": "group_test",
            "produced_deadletters": null,
            "produced_messages": null,
            "queue_id": "e4508dbd-75ba-4199-970e-b1efdb1f4503"
        }
    }
'''

EXAMPLES = '''
# Create Queue-Group
- opentelekomcloud.cloud.dms_queue_group:
    queue_name: 'test-queue'
    group_name: 'test-group'
    state: present

# Delete Queue-Group
- opentelekomcloud.cloud.dms_queue_group:
    queue_name: 'test-queue'
    group_name: 'test-group'
    state: absent
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DmsQueueModule(OTCModule):
    argument_spec = dict(
        queue_name=dict(required=True),
        group_name=dict(required=True),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        attrs = {}
        queue = self.conn.dms.find_queue(name_or_id=self.params['queue_name'])
        if not queue:
            self.exit(
                changed=False,
                failed=True,
                message=('No Queue with name or ID %s found') % (self.params['queue_name'])
            )
        queue_group = self.conn.dms.find_group(queue=queue, name_or_id=self.params['group_name'], ignore_missing=True)

        if self.params['state'] == 'present':

            # Queue-Group creation
            if not queue_group:
                attrs['queue'] = queue.id
                attrs['name'] = self.params['group_name']

                if self.ansible.check_mode:
                    self.exit(changed=True)
                group = self.conn.dms.create_group(**attrs)
                self.exit(changed=True, group=group)

            # Queue-Group Modification - not possible
            elif queue:
                self.exit(
                    changed=False,
                    failed=True,
                    message=('A Queue-Group with this name already exists. Aborting')
                )

        if self.params['state'] == 'absent':

            # Queue-Group Deletion
            if queue_group:
                attrs['queue'] = queue.id
                attrs['group'] = queue_group.id

                if self.ansible.check_mode:
                    self.exit(changed=True)
                queue = self.conn.dms.delete_group(**attrs)
                self.exit(changed=True)

            elif not queue_group:
                self.exit(
                    changed=False,
                    failed=True,
                    message=('No Queue-Group with name or ID %s found') % (self.params['name'])
                )


def main():
    module = DmsQueueModule()
    module()


if __name__ == "__main__":
    main()
