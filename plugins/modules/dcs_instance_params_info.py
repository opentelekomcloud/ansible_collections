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
module: dcs_instance_params_info
short_description: Get Instance Params
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.3.0"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Get Instance Statistics
requirements: ["openstacksdk", "otcextensions"]
options:
  id:
    description:
      - Instance ID of the chosen DCS Instance
    type: str
    required: true
'''

RETURN = '''
instances:
    description: Dictionary of Metrics
    returned: changed
    type: list
    sample: [
        {
            "status": "RUNNING",
            "instance_id": "c08fdc6e-5c25-4185-ab57-c0a5529b727f",
            "redis_config": [
                {
                    "description": "How Redis will select what to remove when maxmemory is reached, You can select among five behaviors...",
                    "param_id": 2,
                    "param_name": "maxmemory-policy",
                    "param_value": "noeviction",
                    "default_value": "noeviction",
                    "value_type": "Enum",
                    "value_range": "volatile-lru,allkeys-lru,volatile-random,allkeys-random,volatile-ttl,noeviction"
                },
                {
                    "description": "Hashes are encoded using a memory efficient data structure when they have a small number of entries",
                    "param_id": 3,
                    "param_name": "hash-max-ziplist-entries",
                    "param_value": "512",
                    "default_value": "512",
                    "value_type": "Interger",
                    "value_range": "1-10000"
                },
                {
                    "description": "Hashes are encoded using a memory efficient data structure when the biggest entry does not exceed a given threshold",
                    "param_id": 4,
                    "param_name": "hash-max-ziplist-value",
                    "param_value": "64",
                    "default_value": "64",
                    "value_type": "Interger",
                    "value_range": "1-10000"
                },
                {
                    "description": "Lists are encoded using a memory efficient data structure when they have a small number of entries",
                    "param_id": 5,
                    "param_name": "list-max-ziplist-entries",
                    "param_value": "512",
                    "default_value": "512",
                    "value_type": "Interger",
                    "value_range": "1-10000"
                },
                {
                    "description": "Lists are encoded using a memory efficient data structure when the biggest entry does not exceed a given threshold",
                    "param_id": 6,
                    "param_name": "list-max-ziplist-value",
                    "param_value": "64",
                    "default_value": "64",
                    "value_type": "Interger",
                    "value_range": "1-10000"
                },
                {
                    "description": "When a set is composed of just strings that happen to be integers in radix 10 in the range of 64 bit signed integers.",
                    "param_id": 7,
                    "param_name": "set-max-intset-entries",
                    "param_value": "512",
                    "default_value": "512",
                    "value_type": "Interger",
                    "value_range": "1-10000"
                },
                {
                    "description": "Sorted sets are encoded using a memory efficient data structure when they have a small number of entries",
                    "param_id": 8,
                    "param_name": "zset-max-ziplist-entries",
                    "param_value": "128",
                    "default_value": "128",
                    "value_type": "Interger",
                    "value_range": "1-10000"
                },
                {
                    "description": "Sorted sets are encoded using a memory efficient data structure when the biggest entry does not exceed a given threshold",
                    "param_id": 9,
                    "param_name": "zset-max-ziplist-value",
                    "param_value": "64",
                    "default_value": "64",
                    "value_type": "Interger",
                    "value_range": "1-10000"
                },
                {
                    "description": "Close the connection after a client is idle for N seconds (0 to disable)",
                    "param_id": 1,
                    "param_name": "timeout",
                    "param_value": "0",
                    "default_value": "0",
                    "value_type": "Interger",
                    "value_range": "0-7200"
                },
                {
                    "description": "Only events that run in more time than the configured latency-monitor-threshold will be logged as latency spikes...",
                    "param_id": 10,
                    "param_name": "latency-monitor-threshold",
                    "param_value": "0",
                    "default_value": "0",
                    "value_type": "Interger",
                    "value_range": "0-86400000"
                },
                {
                    "description": "The total memory, in bytes, reserved for non-data usage.",
                    "param_id": 12,
                    "param_name": "reserved-memory",
                    "param_value": "0",
                    "default_value": "0",
                    "value_type": "Interger",
                    "value_range": "0-6553"
                },
                {
                    "description": "Redis can notify Pub or Sub clients about events happening in the key space",
                    "param_id": 13,
                    "param_name": "notify-keyspace-events",
                    "param_value": null,
                    "default_value": null,
                    "value_type": "regular",
                    "value_range": "([KE]+([A]|[g$lshzxe]+)){0,11}"
                }
            ],
            "config_status": "SUCCESS",
            "config_time": ""
        }
    ]
'''

EXAMPLES = '''
# Query Params
- opentelekomcloud.cloud.dcs_instance_params_info:
        id: 12345678-20fb-441b-a0cd-46369a9f7db0
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DcsInstanceParamsInfoModule(OTCModule):
    argument_spec = dict(
        id=dict(required=True)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        data = []

        for raw in self.conn.dcs.instance_params(self.params['id']):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            instances=data
        )


def main():
    module = DcsInstanceParamsInfoModule()
    module()


if __name__ == '__main__':
    main()
