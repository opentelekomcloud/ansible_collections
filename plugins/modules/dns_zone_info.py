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
module: dns_zone_info
short_description: Get DNS Zone Infos
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.2.1"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Get NAT gateway info from the OTC.
options:
  description:
    description:
      - DNS Zone Description
    type: str
  email:
    description:
      - DNS Zone EMail Adress of the administrator managing the zone
    type: str
  name:
    description:
      - DNS Zone Name
    type: str
  pool_id:
    description:
      - Pool ID of the zone
    type: str
  project_id:
    description:
      - Project ID of the zone
    type: str
  record_num:
    description:
      - Number of record sets in the zone
    type: int
  serial:
    description:
      - Serial number in the SOA record set in a zone
    type: int
  status:
    description:
      - Ressource status
    type: str
  ttl:
    description:
      - TTL value of the SOA record set in the zone
    type: int
  zone_type:
    description:
      - DNS Zone type
    type: str
    required: true
  zone_id:
    description:
      - DNS Zone ID
    type: str

requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
dns_zones:
  description: List of dictionaries describing NAT gateways.
  type: complex
  returned: On Success.
  contains:
    description:
      description: Description of the zone
      type: str
      sample: "What a great zone"
    email:
      description: DNS Zone EMail Adress of the administrator managing the zone
      type: str
      sample: "email@mail.ru"
    name:
      description: Name of the zone
      type: str
      sample: "MyZone123"
    pool_id:
      description: Pool ID of the zone
      type: str
      sample: "fe4080825c5f1977015c5f26688d0008"
    project_id:
      description: Project ID of the zone
      type: str
      sample: "19f43a84a13b49529d2e2c3646693458"
    record_num:
      description: Number of record sets in the zone
      type: int
      sample: 3
    serial:
      description: Serial number in the SOA record set in a zone
      type: int
      sample: 1
    status:
      description: Ressource Status
      type: str
      sample: "ACTIVE"
    ttl:
      description: TTL value of the SOA record set in the zone
      type: int
      sample: 300
    zone_type:
      description: DNS Zone type
      type: str
      sample: "private"
    zone_id:
      description: DNS Zone ID
      type: str
      sample: "fe4080825c5f1977015c5f26688d0008"
    routers:
      description: Routers (VPCs associated with the zone)
      type: dict
      sample: {
        "status": "ACTIVE",
        "router_id": "19664294-0bf6-4271-ad3a-94b8c79c6558",
        "router_region": "xx"
        }

'''

EXAMPLES = '''
# Get list of private zones with 3 records
- name: Listing
  opentelekomcloud.cloud.dns_zone_info:
    record_num: "3"
    zone_type: "private"

'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DNSZoneInfoModule(OTCModule):
    argument_spec = dict(
        description=dict(required=False),
        email=dict(required=False),
        name=dict(required=False),
        pool_id=dict(required=False),
        project_id=dict(required=False),
        record_num=dict(required=False, type='int'),
        serial=dict(required=False, type='int'),
        status=dict(required=False),
        ttl=dict(required=False, type='int'),
        zone_type=dict(required=True),
        zone_id=dict(required=False)
    )

    def run(self):

        data = []
        query = {}

        if self.params['zone_type']:
            query['zone_type'] = self.params['zone_type']

        for raw in self.conn.dns.zones(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        # Filter data by deleting all entries without the right criteria
        i = 0
        while i < len(data):
            if self.params['status']:
                if data[i]['status'] != self.params['status']:
                    del data[i]
                    i = 0
                    continue
            if self.params['record_num']:
                if data[i]['record_num'] != self.params['record_num']:
                    del data[i]
                    i = 0
                    continue
            if self.params['zone_id']:
                if data[i]['zone_id'] != self.params['zone_id']:
                    del data[i]
                    i = 0
                    continue
            if self.params['description']:
                if data[i]['description'] != self.params['description']:
                    del data[i]
                    i = 0
                    continue
            if self.params['email']:
                if data[i]['email'] != self.params['email']:
                    del data[i]
                    i = 0
                    continue
            if self.params['name']:
                if data[i]['name'] != self.params['name']:
                    del data[i]
                    i = 0
                    continue
            if self.params['ttl']:
                if data[i]['ttl'] != self.params['ttl']:
                    del data[i]
                    i = 0
                    continue
            if self.params['serial']:
                if data[i]['serial'] != self.params['serial']:
                    del data[i]
                    i = 0
                    continue
            if self.params['pool_id']:
                if data[i]['pool_id'] != self.params['pool_id']:
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
            dns_zones=data
        )


def main():
    module = DNSZoneInfoModule()
    module()


if __name__ == '__main__':
    main()
