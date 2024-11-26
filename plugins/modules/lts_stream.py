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
module: lts_stream
short_description: Manage LTS log steam on Open Telekom Cloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.1.x"
author: "Daniela Ebert"
description:
  - Manage LTS log stream on Open Telekom Cloud
options:
  log_group_name:
    description:
      - Name of the log group
    type: str
    required: true
  log_stream_name:
    description:
      - Name of the log stream
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
log_stream_id:
    description: ID of the newly created log stream
    type: str
    sample: {
        {
        "log_stream_id": "xxxxxxxx-8165-449a-9e7e-xxxxxxxxxxxx"
        }
    }
'''

EXAMPLES = '''
# Create LTS log stream
- opentelekomcloud.cloud.lts_stream:
    log_group_name: 'lts-test-group'
    log_stream_name: 'lts-test-stream'
    ttl_in_days: '5'
# Delete LTS log stream
- opentelekomcloud.cloud.lts_stream:
    log_group_name: 'lts-test-group'
    log_stream_name: 'lts-test-stream'
    state: absent

'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class LtsStreamModule(OTCModule):
    argument_spec = dict(
        log_group_name=dict(required=True),
        log_stream_name=dict(required=True),
        ttl_in_days=dict(required=False, default='7'),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        group = ""
        stream = ""
        group_list = []
        groupid_list = []
        stream_list = []
        streamid_list = []

        # Get existing log groups with id's
        for x in self.conn.lts.groups():
            group_list.append(x.name)
            groupid_list.append(x.id)

        # Check if log group exists, get id
        if self.params['log_group_name'] in group_list:
            group = self.params['log_group_name']
            i = group_list.index(group)
            groupid = groupid_list[i]

        # Exit, if log group not existing
        if not group:
            self.exit(
                changed=False,
                failed=True,
                message=('No Group with name %s found') % (self.params['log_group_name'])
            )
        # Get existing streams
        for x in self.conn.lts.streams(log_group=groupid):
            stream_list.append(x.name)
            streamid_list.append(x.id)

        # Check if log stream exists, get id
        if self.params['log_stream_name'] in stream_list:
            stream = self.params['log_stream_name']
            i = stream_list.index(stream)
            streamid = streamid_list[i]

        if self.params['state'] == 'present':

            # Stream creation
            if not stream:
                if self.ansible.check_mode:
                    self.exit(changed=True)
                attrs = {
                    'log_group': groupid,
                    'log_stream_name': self.params['log_stream_name'],
                    'ttl_in_days': self.params['ttl_in_days']
                }
                stream = self.conn.lts.create_stream(**attrs)
                self.exit(changed=True, stream=stream.to_dict())

            elif stream:
                self.exit(
                    changed=False,
                    failed=True,
                    message=('Stream with name %s already exists') % (self.params['log_stream_name'])
                )

        if self.params['state'] == 'absent':

            # Stream Deletion
            if stream:
                if self.ansible.check_mode:
                    self.exit(changed=True)
                stream = self.conn.lts.delete_stream(log_group=groupid, log_stream=streamid)
                self.exit(changed=True, stream=stream)

            elif not stream:
                self.exit(
                    changed=False,
                    failed=True,
                    message=('No Stream with name %s found') % (self.params['log_stream_name'])
                )


def main():
    module = LtsStreamModule()
    module()


if __name__ == "__main__":
    main()
