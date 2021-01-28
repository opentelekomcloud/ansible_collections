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
module: dns_recordset_info
short_description: Get DNS Recordsets
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.2.1"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Get DNS Recordsets from the OTC.
options:
  default:
    description:
      - Whether the record set is created by default
    type: bool
  description:
    description:
      - Description of the Record Set
    type: str
  created_at:
    description:
      - Time of creation
    type: str
  name:
    description:
      - Record name or ID
    type: str
  project_id:
    description:
      - Project ID
    type: str
  status:
    description:
      - Resource status
    type: str
  ttl:
    description:
      - Record set cache duration (in second) on a local DNS server
    type: int
  type:
    description:
      - Record set type
    type: str
  updated_at:
    description:
      - Last Update time
    type: str
  zone_id:
    description:
      - Zone ID or Name of the record set
    type: str
    required: true

requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
recordsets:
  description: Get DNS Recordsets
  type: complex
  returned: On Success.
  contains:
    default:
      description: Whether the record set is created by default
      type: str
      sample: "false"
    description:
      description: Description of the Record
      type: str
      sample: "MyRecord123"
    created_at:
      description: Time of creation
      type: str
      sample: "2020-09-29T12:28:59.721"
    name:
      description: Recordset name or ID
      type: str
      sample: "fe80823273f2065d0174defcbdce5951"
    project_id:
      description: Project ID
      type: str
      sample: "16e23f43a13b49529d2e2c3646691288"
    status:
      description: Resource status
      type: str
      sample: "ACTIVE"
    ttl:
      description: Record set cache duration (in second) on a local DNS server
      type: int
      sample: 300
    type:
      description: Record set type
      type: str
      sample: "AAAA"
    updated_at:
      description: Last Update time
      type: str
      sample: "2020-09-29T12:28:59.721"
    zone_id:
      description: Zone ID of the record set
      type: str
      sample: "fe4080825c5f1234015c5f26688d0008"

'''

EXAMPLES = '''
# Get Record Set Info:
- name: Record Set Info
  opentelekomcloud.cloud.dns_recordset_info:
    zone_id: "fe12345672701c340174d8e94bb9562c"
    name: "my"
    ttl: 86400
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DNSRecordsetsInfoModule(OTCModule):
    argument_spec = dict(
        zone_id=dict(required=True),
        status=dict(required=False),
        type=dict(required=False),
        name=dict(required=False),
        description=dict(required=False),
        ttl=dict(required=False, type='int'),
        created_at=dict(required=False),
        updated_at=dict(required=False),
        default=dict(required=False, type='bool'),
        project_id=dict(required=False)
    )

    def run(self):

        data = []
        query = {}

        if self.params['status']:
            query['status'] = self.params['status']
        if self.params['type']:
            query['type'] = self.params['type']
        if self.params['name']:
            query['name'] = self.params['name']

        for raw in self.conn.dns.recordsets(zone=self.params['zone_id'], **query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        # Filter data by deleting all entries without the right criteria
        i = 0
        while i < len(data):
            if self.params['description']:
                if data[i]['description'] != self.params['description']:
                    del data[i]
                    i = 0
                    continue
            if self.params['ttl']:
                if data[i]['ttl'] != self.params['ttl']:
                    del data[i]
                    i = 0
                    continue
            if self.params['created_at']:
                if data[i]['created_at'] != self.params['created_at']:
                    del data[i]
                    i = 0
                    continue
            if self.params['updated_at']:
                if data[i]['updated_at'] != self.params['updated_at']:
                    del data[i]
                    i = 0
                    continue
            if self.params['default']:
                if data[i]['default'] != self.params['default']:
                    del data[i]
                    i = 0
                    continue
            if self.params['project_id']:
                if data[i]['project_id'] != self.params['project_id']:
                    del data[i]
                    i = 0
                    continue
            i = i + 1

        self.exit(
            changed=False,
            recordsets=data
        )


def main():
    module = DNSRecordsetsInfoModule()
    module()


if __name__ == '__main__':
    main()
