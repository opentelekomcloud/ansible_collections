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
module: dms_instance_info
short_description: Get info about DMS instances
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.1.2"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Get info about DMS instances
options:
  engine:
    description:
      - Name of the Engine
    type: str
  name:
    description:
      - Name
    type: str
  id:
    description:
      - ID of the Instance
    type: str
  status:
    description:
      - Instance Status
    type: str
  includeFailure:
    description:
      - Indicates whether to return instances that fail to be created.
    type: bool
    default: true
  exactMatchName:
    description:
      - Indicates whether to search for the instance that precisely matches a specified instance name.
    type: bool
    default: false
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
dms_queues:
    description: Dictionary of Queue Groups
    returned: changed
    type: list
    sample: [
        {
            "access_user": null,
            "availability_zones": [
                "12345678"
            ],
            "charging_mode": 1,
            "connect_address": "",
            "created_at": "1617183440086",
            "description": null,
            "engine_name": "kafka",
            "engine_version": "2.3.0",
            "id": "12345678-003f-4d2a-9f6a-8468f832faea",
            "instance_id": "12345678-003f-4d2a-9f6a-8468f832faea",
            "is_public": false,
            "is_ssl": false,
            "kafka_public_status": "false",
            "maintenance_end": "02:00:00",
            "maintenance_start": "22:00:00",
            "max_partitions": 300,
            "name": "kafka-4ck1",
            "network_id": "12345678-99ee-43aa-9448-6fac41614db6",
            "password": null,
            "port": 9092,
            "product_id": "00300-30308-0--0",
            "public_bandwidth": 0,
            "retention_policy": "produce_reject",
            "router_id": "12345678-6d1d-471e-a911-6924b7ec6ea9",
            "router_name": "abcdef",
            "security_group_id": "12345678-a836-4dc9-ae59-0aea6dcaf0c3",
            "security_group_name": "sg",
            "service_type": "advanced",
            "spec": "100MB",
            "spec_code": "dms.instance.kafka.cluster.c3.mini",
            "status": "CREATING",
            "storage": 600,
            "storage_resource_id": "12345678-f432-4409-8c1b-f1a40fba7408",
            "storage_spec_code": "dms.physical.storage.high",
            "storage_type": "hec",
            "total_storage": 600,
            "type": "cluster",
            "used_storage": 0,
            "user_id": "12345678",
            "user_name": "test"
        }
    ]
'''

EXAMPLES = '''
# Query all Instances
- opentelekomcloud.cloud.dms_instance_info:
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DmsInstanceInfoModule(OTCModule):
    argument_spec = dict(
        engine=dict(required=False),
        name=dict(required=False),
        id=dict(required=False),
        status=dict(required=False),
        includeFailure=dict(required=False, type='bool', default='true'),
        exactMatchName=dict(required=False, type='bool', default='false'),
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):

        data = []
        query = {}

        if self.params['engine']:
            query['engine'] = self.params['engine']
        if self.params['name']:
            query['name'] = self.params['name']
        if self.params['id']:
            query['id'] = self.params['id']
        if self.params['status']:
            query['status'] = self.params['status']
        if self.params['includeFailure']:
            query['includeFailure'] = self.params['includeFailure']
        if self.params['exactMatchName']:
            query['exactMatchName'] = self.params['exactMatchName']

        for raw in self.conn.dms.instances(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)
        self.exit(
            changed=False,
            dms_instances=data
        )


def main():
    module = DmsInstanceInfoModule()
    module()


if __name__ == '__main__':
    main()
