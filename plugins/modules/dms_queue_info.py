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
module: dms_queue_info
short_description: Get info about DMS queues
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.1.2"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Get info about DMS queues
options:
  queue:
    description:
      - Name or ID of a target queue. Leave it empty to query all queues.
    type: str
    required: false
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
dms_queues:
    description: Dictionary of Queues
    returned: changed
    type: list
    sample: [
        {
            "created": 1517385090349,
            "description": "",
            "id": "12345678-73e4-449f-a157-53d5d9900e21",
            "max_consume_count": null,
            "name": "test-test",
            "queue_mode": "NORMAL",
            "redrive_policy": null,
            "retention_hours": null
        }
    ]
'''

EXAMPLES = '''
# Query a single DMS Queue
- opentelekomcloud.cloud.dms_queue_info:
    queue: 'test-test'
  register: dms-queue
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DmsQueueInfoModule(OTCModule):
    argument_spec = dict(
        queue=dict(required=False)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):

        data = []

        if self.params['queue']:
            queue = self.conn.dms.find_queue(
                name_or_id=self.params['queue']
            )
            if queue:
                dt = queue.to_dict()
                dt.pop('location')
                data.append(dt)
            else:
                self.exit(
                    changed=False,
                    failed=True,
                    message=('No Queue found with ID or Name: %s' %
                             self.params['queue'])
                )
        else:
            for raw in self.conn.dms.queues():
                dt = raw.to_dict()
                dt.pop('location')
                data.append(dt)

        self.exit(
            changed=False,
            dms_queues=data
        )


def main():
    module = DmsQueueInfoModule()
    module()


if __name__ == '__main__':
    main()
