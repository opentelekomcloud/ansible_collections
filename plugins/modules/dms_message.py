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
module: dms_message
short_description: Manage DMS Messages on Open Telekom Cloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.1.2"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Manage DMS Messages on Open Telekom Cloud
options:
  queue:
    description:
      - Name of the Queue. Can also be ID.
    type: str
    required: true
  group:
    description:
      - Name of the Group. Can also be ID. Required when consuming.
    type: str
    required: false
  messages:
    description:
      - Messages.
    type: list
    elements: dict
    required: false
  max_msgs:
    description:
      - Max messages to consume.
    type: int
    required: false
    default: 10
  time_wait:
    description:
      - Time to wait for consuming.
    type: int
    required: false
    default: 3
  ack_wait:
    description:
      - Time to wait for confirmation.
    type: int
    required: false
    default: 30
  ack:
    description:
      - Whether to try confirming the consumed messages or not.
    type: bool
    required: false
    default: True
  task:
    choices: [send, consume]
    description: Task to do
    type: str
    required: True
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
message:
    description: Dictionary of DMS Queue
    returned: changed
    type: dict
    sample: {
        "message": [
            {
                "attributes": {},
                "body": "test2",
                "error": null,
                "error_code": null,
                "handler": null,
                "id": "eyJ0b3BpYyI6InEtMTZkNTNhODRhMTNiNDk1MjlkMmUyYzM2N....",
                "location": null,
                "name": null,
                "state": null
            },
            {
                "attributes": {},
                "body": "test1",
                "error": null,
                "error_code": null,
                "handler": null,
                "id": "eyJ0b3BpYyI6InEtMTZkNTNhODRhMTNiNDk1MjlkMmUyYzM2N...",
                "location": null,
                "name": null,
                "state": null
            }
        ]
    }
'''

EXAMPLES = '''
# Send Message
- opentelekomcloud.cloud.dms_message:
    queue: 'queue'
    messages:
        - body: 'test1'
          attributes:
            attribute1: 'value1'
            attribute2: 'value2'
        - body: 'test2'
          attributes:
            attribute1: 'value3'
            attribute2: 'value4'
    task: send

# Consume Message
- opentelekomcloud.cloud.dms_message:
    queue: 'queue'
    group: 'group'
    task: consume
    ack: false
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DmsMessageModule(OTCModule):
    argument_spec = dict(
        queue=dict(required=True),
        group=dict(required=False),
        messages=dict(required=False, type='list', elements='dict'),
        max_msgs=dict(required=False, type='int', default=10),
        time_wait=dict(required=False, type='int', default=3),
        ack_wait=dict(required=False, type='int', default=30),
        ack=dict(required=False, type='bool', default='True'),
        task=dict(type='str', choices=['send', 'consume'], required=True)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        attrs = {}
        queue = self.conn.dms.find_queue(name_or_id=self.params['queue'])
        if not queue:
            self.exit(
                changed=False,
                failed=True,
                message=('No Queue with name or ID %s found') % (self.params['queue_name'])
            )

        if self.params['task'] == 'send':

            attrs['queue'] = queue.id
            attrs['messages'] = self.params['messages']
            if self.ansible.check_mode:
                self.exit(changed=True)
            message = self.conn.dms.send_messages(**attrs)
            self.exit(changed=True, message=message)

        if self.params['task'] == 'consume':

            if not self.params['group']:
                self.exit(
                    changed=False,
                    failed=True,
                    message=('No Group name or ID specified')
                )
            queue_group = self.conn.dms.find_group(queue=queue, name_or_id=self.params['group'], ignore_missing=True)
            if not queue_group:
                self.exit(
                    changed=False,
                    failed=True,
                    message=('No Queue-Group with name or ID %s found') % (self.params['group'])
                )
            attrs['queue'] = queue.id
            attrs['group'] = queue_group.id
            attrs['max_msgs'] = self.params['max_msgs']
            attrs['time_wait'] = self.params['time_wait']
            attrs['ack_wait'] = self.params['ack_wait']
            if self.ansible.check_mode:
                self.exit(changed=True)
            response = []
            for message in self.conn.dms.consume_message(**attrs):
                dt = message.to_dict()
                response.append(dt)

            if self.params['ack'] is False:
                self.exit(changed=True, message=response)
            else:
                messages = {
                    'handler': response[0]['id'],
                    'status': 'success'
                }
                result = self.conn.dms.ack_message(queue=queue, group=queue_group, messages=messages)
                response.append(result)
                self.exit(changed=True, message=response)


def main():
    module = DmsMessageModule()
    module()


if __name__ == "__main__":
    main()
