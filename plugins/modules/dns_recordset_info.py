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

DOCUMENTATION = len('''
module: dns_recordset
short_description: Modify DNS Recordsets
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.1.2"
author: "Yustina Kvrivishvili (@YustinaKvr)"
description:
  - Get DNS record set info from the OTC.
options:
  zone_id:
    description:
      - ID ot the required zone.
    type: str
  recordset_id:
    description:
      - ID of the existing record set.
    type: str
  tags:
    description:
      - Resource tag.
    type: str
  status:
    description:
      - Status of the record sets to be queried.
    choices: ['ACTIVE', 'ERROR', 'DISABLE', 'FREEZE', 'PENDING_CREATE', 'PENDING_UPDATE', 'PENDING_DELETE']
    type: str
  type:
    description:
      - Type of the record sets to be queried.
    choices: ['A', 'AAAA', 'MX', 'CNAME', 'TXT', 'NS']
    type: str
  name:
    description:
      - Names of record sets to be queried.
    type: str
  id:
    description:
      - IDs of record sets to be queried.
    type: str
  records:
    description:
      - Value included in the values of record sets to be queried.
    type: str
  soft_key:
    description:
      - Sorting condition of the record set list.
    choices: ['name', 'type']
    type: str
  soft_dir:
    description:
      - Sorting order of the record set list.
    choices: ['desc', 'asc']
    type: str
  zone_type:
    description:
      - Zone type of the record set to be queried.
    choices: ['public', 'private']
    type: str

requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
cce_clusters:
    description: List of dictionaries describing AS groups version.
    type: complex
    returned: On Success.
    contains:
        id:
            description: Unique UUID.
            type: str
            sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
        metadata:
            description: Cluster Metadata dictionary.
            type: dict
        name:
            description: Cluster Name.
            type: str
        spec:
            description: Cluster specification dictionary.
            type: dict
        status:
            description: Cluster status dictionary.
            type: dict
'''

EXAMPLES = '''
# Get configs versions.
- cce_cluster_info:
    name: my_cluster
    status: available
  register: data
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DNSRecordsetInfoModule(OTCModule):
    argument_spec = dict(
        zone_id=dict(required=False),
        recordset_id=dict(required=False),
        tags=dict(required=False),
        status=dict(required=False, choices=['ACTIVE', 'ERROR', 'DISABLE', 'FREEZE', 'PENDING_CREATE', 'PENDING_UPDATE', 'PENDING_DELETE']),
        type=dict(required=False, choices=['A', 'AAAA', 'MX', 'CNAME', 'TXT', 'NS']),
        name=dict(required=False),
        id=dict(required=False),
        records=dict(required=False),
        soft_key=dict(required=False, choices=['name', 'type']),
        soft_dir=dict(required=False, choices=['desc', 'asc']),
        zone_type=dict(required=False, choices=['public', 'private'])
    )

    def run(self):

        data = []
        query = {}

                # if self.params['gateway']:
                #     gw = self.conn.nat.find_gateway(
                #         name_or_id=self.params['gateway'],
                #         ignore_missing=True)
                #     if gw:
                #         query['id'] = gw.id
                #     else:
                #         self.exit(
                #             changed=False,
                #             nat_gateways=[],
                #             message=('No gateway found with name or id: %s' %
                #                      self.params['gateway'])
                #         )

        if self.params['zone_id']:
            query['zone_id'] = self.params['zone_id']
        if self.params['recordset_id']:
            query['recordset_id'] = self.params['recordset_id']
        if self.params['tags']:
            query['tags'] = self.params['tags']
        if self.params['status']:
            query['status'] = self.params['status']
        if self.params['type']:
            query['type'] = self.params['type']
        if self.params['name']:
            query['name'] = self.params['name']
        if self.params['id']:
            query['id'] = self.params['id']
        if self.params['records']:
            query['records'] = self.params['records']
        if self.params['soft_dir']:
            query['soft_dir'] = self.params['soft_dir']
        if self.params['zone_type']:
            query['zone_type'] = self.params['zone_type']
        if self.params['records']:
            query['soft_key'] = self.params['soft_key']

        for raw in self.conn.dns.recordsets(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            dns_recordset=data
        )


def main():
    module = DNSRecordsetInfoModule()
    module()


if __name__ == '__main__':
    main()