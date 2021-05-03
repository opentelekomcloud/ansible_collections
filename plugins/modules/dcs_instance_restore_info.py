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
module: dcs_instance_restore_info
short_description: Get Instance Restore infos
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.3.0"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Get Instance Restore infos
requirements: ["openstacksdk", "otcextensions"]
options:
  id:
    description:
      - Instance ID of the chosen DCS Instance
    type: str
    required: true
  beginTime:
    description:
      - Beginning Time of the query search
    type: str
    required: false
  endTime:
    description:
      - End Time of the query search
    type: str
    required: false
'''

RETURN = '''
instances:
    description: Dictionary of Metrics
    returned: changed
    type: list
    sample: [
        {
            "backup_description": null,
            "backup_id": "12345678-f021-417f-b019-dc02182926a9",
            "backup_name": "backup_20210302142342",
            "created_at": "2021-03-02T13:57:56.194Z",
            "description": null,
            "error_code": null,
            "id": "12345678-05c3-42c9-ac09-c2da452372cc",
            "name": null,
            "progress": "100.00",
            "restore_description": null,
            "restore_name": "restore_20210302145756",
            "status": "succeed",
            "updated_at": "2021-03-02T13:58:20.382Z"
        }

    ]
'''

EXAMPLES = '''
# Query Params
- opentelekomcloud.cloud.dcs_instance_restore_info:
        id: 12345678-20fb-441b-a0cd-46369a9f7db0
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DcsInstanceRestoreInfoModule(OTCModule):
    argument_spec = dict(
        id=dict(required=True),
        beginTime=dict(required=False),
        endTime=dict(required=False)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        data = []
        query = {}

        query['instance'] = self.params['id']
        if self.params['beginTime']:
            query['beginTime'] = self.params['beginTime']
        if self.params['endTime']:
            query['endTime'] = self.params['endTime']

        for raw in self.conn.dcs.restore_records(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            instances=data
        )


def main():
    module = DcsInstanceRestoreInfoModule()
    module()


if __name__ == '__main__':
    main()
