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
module: dns_floating_ip_info
short_description: Get DNS PTR Records
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.2.1"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Get DNS PTR Records from the OTC.
options:
  address:
    description:
      - EIP address
    type: str
  description:
    description:
      - Description of the Record
    type: str
  id:
    description:
      - PTR record ID
    type: str
  ptrdname:
    description:
      - Domain name of the PTR record
    type: str
  status:
    description:
      - Resource status
    type: str
  ttl:
    description:
      - PTR record cache duration (in second) on a local DNS server
    type: int

requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
ptr_records:
  description: Get DNS PTR Records
  type: complex
  returned: On Success.
  contains:
    address:
      description: EIP address
      type: str
      sample: "100.138.123.199"
    description:
      description: Description of the Record
      type: str
      sample: "MyRecord123"
    id:
      description: PTR record id
      type: str
      sample: "eu-de:fe864230-d3bc-4391-8a32-394c3e9ca22d"
    ptrdname:
      description: Domain name of the PTR record
      type: str
      sample: "example.com"
    status:
      description: Resource status
      type: str
      sample: "ACTIVE"
    ttl:
      description: PTR record cache duration (in second) on a local DNS server
      type: int
      sample: 300

'''

EXAMPLES = '''
# Get PRT Info:
- name: Getting Info
  opentelekomcloud.cloud.dns_floating_ip_info:
    description: "Test"
    ptrdname: "example.com"

'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DNSFloatingIpInfoModule(OTCModule):
    argument_spec = dict(
        address=dict(required=False),
        description=dict(required=False),
        id=dict(required=False),
        ptrdname=dict(required=False),
        status=dict(required=False),
        ttl=dict(required=False, type='int')
    )

    def run(self):

        query = {}
        data = []

        if self.params['address']:
            query['address'] = self.params['address']
        if self.params['id']:
            query['id'] = self.params['id']
        if self.params['ptrdname']:
            query['ptrdname'] = self.params['ptrdname']
        if self.params['ttl']:
            query['ttl'] = self.params['ttl']
        if self.params['description']:
            query['description'] = self.params['description']
        if self.params['status']:
            query['status'] = self.params['status']

        for raw in self.conn.dns.floating_ips(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            ptr_records=data
        )


def main():
    module = DNSFloatingIpInfoModule()
    module()


if __name__ == '__main__':
    main()
