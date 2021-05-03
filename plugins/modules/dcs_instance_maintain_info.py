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
module: dcs_instance_maintain_info
short_description: Get Instance Maintenance Informations
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.3.0"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Get Instance Maintenance Informations
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
instances:
    description: Dictionary of Metrics
    returned: changed
    type: list
    sample: [
            {
            "created_at": "2021-03-02T13:23:42.968Z",
            "description": null,
            "error_code": null,
            "id": "c417bd7d-f021-417f-b019-dc02182926a9",
            "name": "backup_20210302142342",
            "period": null,
            "progress": "100.00",
            "size": 124,
            "status": "succeed",
            "type": "manual",
            "updated_at": "2021-03-02T13:25:30.723Z"
        }
    ]
'''

EXAMPLES = '''
# Query Params
- opentelekomcloud.cloud.dcs_instance_backup_info:
        id: 12345678-20fb-441b-a0cd-46369a9f7db0
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DcsInstanceMaintainInfoModule(OTCModule):
    argument_spec = dict(
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        data = []

        # for raw in self.conn.dcs.backups(self.params['id']):
        #     dt = raw.to_dict()
        #     dt.pop('location')
        #     data = dt

        self.exit(
            changed=False,
            instances=data
        )


def main():
    module = DcsInstanceMaintainInfoModule()
    module()


if __name__ == '__main__':
    main()
