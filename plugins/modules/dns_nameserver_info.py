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
module: dns_nameserver_info
short_description: Get DNS Nameserver Infos
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.2.1"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Get DNS Namerserver infos from the OTC.
options:
  address:
    description:
      - IP address of a DNS Server
    type: str
  hostname:
    description:
      - Hostname of a DNS server
    type: str
  priority:
    description:
      - Priority of a name server
    type: str
  zone:
    description:
      - DNS Zone ID
    type: str
    required: true

requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
dns_nameservers:
  description: List of DNS Nameservers
  type: complex
  returned: On Success.
  contains:
    address:
      description: IP address of a DNS server
      type: str
      sample: "100.138.123.199"
    hostname:
      description: Hostname of a DNS server
      type: str
      sample: "Myhostname"
    priority:
      description: Priority of a name server
      type: str
      sample: "1"
    zone:
      description: Specifies the DNS zone
      type: str
      sample: "fe40808272701cbe0172cbca17f91882"
'''

EXAMPLES = '''
# Get Nameserver Info about a zone:

- name: Get nameserver Info
  opentelekomcloud.cloud.dns_nameserver_info:
    zone: fe40808272701cbe0172cbca17f91882
    hostname: "MyHostname"

'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DNSNameserverInfoModule(OTCModule):
    argument_spec = dict(
        address=dict(required=False),
        hostname=dict(required=False),
        priority=dict(required=False),
        zone=dict(required=True)
    )

    def run(self):

        data = []
        query = {}

        if self.params['zone']:
            zi = self.conn.dns.find_zone(
                name_or_id=self.params['zone'],
                ignore_missing=True)
            if zi:
                query['zone'] = zi.id
            else:
                self.exit(
                    changed=False,
                    message=('No zone found with name or id: %s' %
                             self.params['zone'])
                )

        for raw in self.conn.dns.nameservers(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        # Filter data by deleting all entries without the right criteria as our Query doesn't support other queries
        i = 0
        while i < len(data):
            if self.params['address']:
                if data[i]['address'] != self.params['address']:
                    del data[i]
                    i = 0
                    continue
            if self.params['hostname']:
                if data[i]['hostname'] != self.params['hostname']:
                    del data[i]
                    i = 0
                    continue
            if self.params['priority']:
                if data[i]['priority'] != self.params['priority']:
                    del data[i]
                    i = 0
                    continue
            i = i + 1

        self.exit(
            changed=False,
            dns_nameservers=data
        )


def main():
    module = DNSNameserverInfoModule()
    module()


if __name__ == '__main__':
    main()
