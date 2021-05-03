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
module: dcs_instance_info
short_description: Get Instance Informations
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.3.0"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Get Instance Informations
options:
  id:
    description:
      - Instance ID of the chosen DCS Instance
    type: str
    required: false
  status:
    description:
      - Status of the chosen DCS Instance
    type: str
    required: false
  name:
    description:
      - Name of the chosen DCS Instance
    type: str
    required: false
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
instances:
    description: Dictionary of Metrics
    returned: changed
    type: list
    sample: [
        {
            "available_zones": null,
            "backup_policy": null,
            "capacity": 2,
            "charging_mode": 0,
            "created_at": "2021-02-26T08:21:49.137Z",
            "description": null,
            "domain_name": null,
            "engine": "Redis",
            "engine_version": "3.0",
            "error_code": null,
            "id": "6543212f-6bd4-45df-9c4e-fadb35d6e0d0",
            "internal_version": null,
            "ip": "192.168.10.12",
            "lock_time": null,
            "lock_time_left": null,
            "maintain_begin": "02:00:00",
            "maintain_end": "06:00:00",
            "max_memory": 1536,
            "message": null,
            "name": "dcs-qrt6",
            "order_id": null,
            "password": null,
            "port": 6379,
            "product_id": null,
            "resource_spec_code": "dcs.master_standby",
            "result": null,
            "retry_times_left": null,
            "security_group_id": "6543212f-b782-4aff-8311-19896597fd4e",
            "security_group_name": null,
            "status": "RUNNING",
            "subnet_cidr": null,
            "subnet_id": null,
            "subnet_name": null,
            "used_memory": 4,
            "user_id": "1234567890bb4c6f81bc358d54693962",
            "user_name": "user",
            "vpc_id": "12345678-dc40-4e3a-95b1-5a0756441e12",
            "vpc_name": null
        }
    ]
'''

EXAMPLES = '''
# Query Instance Informations from DCS Instance with ID
- opentelekomcloud.cloud.dcs_instance_info:
    instance_id: 6543212f-6bd4-45df-9c4e-fadb35d6e0d0

# Query all existing Instances
- opentelekomcloud.cloud.dcs_instance_info:
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DcsInstanceInfoModule(OTCModule):
    argument_spec = dict(
        id=dict(required=False),
        name=dict(required=False),
        status=dict(required=False),
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):

        data = []
        query = {}

        for raw in self.conn.dcs.instances(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        # The API doesn't support queries, but we want to be able to not only list but also look for params of a specific instance
        # This part removes other instances from the data result so that only the one with the given params will be shown
        i = 0
        while i < len(data):
            if self.params['id']:
                if data[i]['id'] != self.params['id']:
                    del data[i]
                    i = 0
                    continue
            if self.params['name']:
                if data[i]['name'] != self.params['name']:
                    del data[i]
                    i = 0
                    continue
            if self.params['status']:
                if data[i]['status'] != self.params['status']:
                    del data[i]
                    i = 0
                    continue
            i = i + 1

        self.exit(
            changed=False,
            instances=data
        )


def main():
    module = DcsInstanceInfoModule()
    module()


if __name__ == '__main__':
    main()
