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
module: dms_queue_group_info
short_description: Get info about DMS queue groups
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.1.2"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Get info about DMS queue groups
options:
  queue:
    description:
      - Name or ID of a target queue. Leave it empty to query all queues.
    type: str
    required: true
  include_deadletter:
    description:
      - Indicates whether to list dead letter parameters in the response message.
    type: bool
    required: false
    default: false
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
dms_queues:
    description: Dictionary of Queue Groups
    returned: changed
    type: list
    sample: [
        {
            "available_deadletters": 0,
            "available_messages": 0,
            "consumed_messages": 0,
            "id": "g-12345678-b770-4ace-83c2-28800b7a4ecc",
            "name": "group-123456754",
            "produced_deadletters": 0,
            "produced_messages": 0
        }
    ]
'''

EXAMPLES = '''
# Query a single DMS Queue Group
- opentelekomcloud.cloud.dms_queue_group_info:
    queue: 'test-test'
    include_deadletter: true
  register: dms-queue
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DmsQueueInfoModule(OTCModule):
    argument_spec = dict(
        queue=dict(required=True),
        include_deadletter=dict(required=False, type='bool', default='false')
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):

        data = []
        query = {}

        queue = self.conn.dms.find_queue(
            name_or_id=self.params['queue']
        )
        if self.params['include_deadletter']:
            query['include_deadletter'] = self.params['include_deadletter']
        if queue:
            for raw in self.conn.dms.groups(queue.id, **query):
                dt = raw.to_dict()
                dt.pop('location')
                data.append(dt)
            self.exit(
                changed=False,
                dms_queues=data
            )
        else:
            self.exit(
                changed=False,
                failed=True,
                message=('No Queue found with ID or Name: %s' %
                         self.params['queue'])
            )


def main():
    module = DmsQueueInfoModule()
    module()


if __name__ == '__main__':
    main()
