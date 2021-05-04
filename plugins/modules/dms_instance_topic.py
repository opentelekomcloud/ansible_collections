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
module: dms_instance_topic
short_description: Manage DMS Instance Topics on Open Telekom Cloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.1.2"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Manage DMS Instance Topics on Open Telekom Cloud
options:
  instance:
    description:
      - Name or ID of the Instance
    type: str
    required: true
  id:
    description:
      - Name of the Instance topic to be created. Required for creation.
    type: str
    required: false
  partition:
    description:
      - Indicates the number of topic partitions, which is used to set the number of concurrently consumed messages.
    type: int
    required: false
    default: 3
  replication:
    description:
      - Indicates the number of replicas, which is configured to ensure data reliability.
    type: int
    required: false
    default: 3
  sync_replication:
    description:
      - Indicates whether to enable synchronous replication.
    type: bool
    required: false
    default: false
  retention_time:
    description:
      - Indicates the retention period of a message.
    type: int
    required: false
    default: 72
  sync_message_flush:
    description:
      - Indicates whether to enable synchronous flushing.
    type: bool
    required: false
    default: false
  topics:
    description:
      - Indicates the list of topics to be deleted. Required for deleting.
    type: list
    required: false
    elements: str
  state:
    choices: [present, absent]
    default: present
    description: Instance state
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
instance:
    description: Dictionary of Instance Topics
    returned: changed
    type: dict
    sample: {
        "topic": {
            "id": "test2",
            "is_sync_flush": null,
            "is_sync_replication": null,
            "location": {
                "cloud": "otc",
                "project": {
                    "domain_id": null,
                    "domain_name": null,
                    "id": "12345678",
                    "name": "eu-de"
                },
                "region_name": "eu-de",
                "zone": null
            },
            "name": null,
            "partition": 3,
            "replication": 3,
            "retention_time": 72
        }
    }
'''

EXAMPLES = '''
# Create Instance Topic
- opentelekomcloud.cloud.dms_instance_topic:
    instance: 'test'
    id: 'test2'

# Delete Instance Topics
- opentelekomcloud.cloud.dms_instance_topic:
    instance: 'test'
    topics:
      - 'test1'
      - 'test2'
    state: absent
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DmsInstanceTopic(OTCModule):
    argument_spec = dict(
        instance=dict(required=True),
        id=dict(required=False),
        topics=dict(required=False, type='list', elements='str'),
        partition=dict(required=False, type='int', default=3),
        replication=dict(required=False, type='int', default=3),
        sync_replication=dict(required=False, type='bool', default=False),
        retention_time=dict(required=False, type='int', default=72),
        sync_message_flush=dict(required=False, type='bool', default=False),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        attrs = {}
        instance = self.conn.dms.find_instance(name_or_id=self.params['instance'], ignore_missing=True)
        if not instance:
            self.exit(
                changed=False,
                failed=True,
                message=('No Instance with name or ID %s found') % (self.params['instance'])
            )

        if self.params['state'] == 'present':

            # Topic creation
            if self.params['id']:
                attrs['id'] = self.params['id']
            else:
                self.exit(
                    changed=False,
                    failed=True,
                    message=('No Topic ID specified, but needed for creation!')
                )
            if self.params['partition']:
                attrs['partition'] = self.params['partition']
            if self.params['replication']:
                attrs['replication'] = self.params['replication']
            if self.params['sync_replication']:
                attrs['sync_replication'] = self.params['sync_replication']
            if self.params['retention_time']:
                attrs['retention_time'] = self.params['retention_time']
            if self.params['sync_message_flush']:
                attrs['sync_message_flush'] = self.params['sync_message_flush']

            if self.ansible.check_mode:
                self.exit(changed=True)
            topic = self.conn.dms.create_topic(instance, **attrs)
            self.exit(changed=True, topic=topic.to_dict())

        if self.params['state'] == 'absent':

            if self.params['topics']:
                # Topic Deletion
                if self.ansible.check_mode:
                    self.exit(changed=True)
                topic = self.conn.dms.delete_topic(instance, self.params['topics'])
                self.exit(changed=True)
            else:
                self.exit(
                    changed=False,
                    failed=True,
                    message=('No Topics specified, but needed for deletion!')
                )


def main():
    module = DmsInstanceTopic()
    module()


if __name__ == "__main__":
    main()
