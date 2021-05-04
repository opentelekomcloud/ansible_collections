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
module: dms_queue
short_description: Manage DMS Queues on Open Telekom Cloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.1.2"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Manage DMS Queues on Open Telekom Cloud
options:
  name:
    description:
      - Name of the Queue. Can also be ID for deletion.
    type: str
    required: true
  queue_mode:
    description:
      - Indicates the queue type.
    type: str
    default: NORMAL
  description:
    description:
      - Description.
    type: str
  redrive_policy:
    description:
      - This parameter specifies whether to enable dead letter messages.
      - Dead letter messages are messages that cannot be normally consumed.
      - This parameter is valid only when queue_mode is set to NORMAL or FIFO.
    type: str
    default: disable
  max_consume_count:
    description:
      - Indicates the maximum number of allowed message consumption failures.
      - This parameter is mandatory only when redrive_policy is set to enable.
    type: int
  retention_hours:
    description:
      - Indicates the hours of storing messages in the Kafka queue.
      - This parameter is valid only when queue_mode is set to KAFKA_HA or KAFKA_HT.
    type: int
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
        "queue": {
            "created": null,
            "description": null,
            "id": "c28ff35a-dbd4-460a-a30d-cf31a6013eb0",
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
            "max_consume_count": null,
            "name": "test-queue",
            "queue_mode": "NORMAL",
            "redrive_policy": "disable",
            "retention_hours": null
        }
    }
'''

EXAMPLES = '''
# Create Queue
- opentelekomcloud.cloud.dms_queue:
    name: 'test-queue'
    state: present

# Delete Queue
- opentelekomcloud.cloud.dms_queue:
    name: 'test-queue'
    state: absent
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DmsQueueModule(OTCModule):
    argument_spec = dict(
        name=dict(required=True),
        queue_mode=dict(required=False, default='NORMAL'),
        description=dict(required=False),
        redrive_policy=dict(required=False, default='disable'),
        max_consume_count=dict(required=False, type='int'),
        retention_hours=dict(required=False, type='int'),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        attrs = {}
        queue = self.conn.dms.find_queue(name_or_id=self.params['name'])

        if self.params['state'] == 'present':

            # Queue creation
            if not queue:
                attrs['name'] = self.params['name']
                if self.params['queue_mode']:
                    attrs['queue_mode'] = self.params['queue_mode']
                if self.params['description']:
                    attrs['description'] = self.params['description']
                if self.params['redrive_policy']:
                    attrs['redrive_policy'] = self.params['redrive_policy']
                if self.params['max_consume_count']:
                    attrs['max_consume_count'] = self.params['max_consume_count']
                if self.params['retention_hours']:
                    attrs['retention_hours'] = self.params['retention_hours']

                if self.ansible.check_mode:
                    self.exit(changed=True)
                queue = self.conn.dms.create_queue(**attrs)
                self.exit(changed=True, queue=queue.to_dict())

            # Queue Modification - not possible
            elif queue:
                self.exit(
                    changed=False,
                    failed=True,
                    message=('A Queue with this name already exists. Aborting')
                )

        if self.params['state'] == 'absent':

            # Queue Deletion
            if queue:
                if self.ansible.check_mode:
                    self.exit(changed=True)
                queue = self.conn.dms.delete_queue(queue=queue.id)
                self.exit(changed=True)

            elif not queue:
                self.exit(
                    changed=False,
                    failed=True,
                    message=('No Queue with name or ID %s found') % (self.params['name'])
                )


def main():
    module = DmsQueueModule()
    module()


if __name__ == "__main__":
    main()
