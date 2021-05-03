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
module: dcs_instance_password
short_description: Manage DCS Instance Passwords on Open Telekom Cloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.8.0"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Manage DCS Instance Passwords on Open Telekom Cloud
options:
  new_password:
    description:
      - New password of the instance
    type: str
    required: true
  old_password:
    description:
      - Old Password of the instance
    type: str
    required: true
  id:
    description:
      - ID or name of the instance
    type: str
    required: true
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
dcs_instance:
    description: Dictionary of DCS instance
    returned: changed
    type: dict
    sample: {

    }
'''

EXAMPLES = '''
# Modify Password
- opentelekomcloud.cloud.dcs_instance:
    id: dcs_test_name
    old_password: "This1st0t4llys4f3!"
    new_password: "Th!7173v3NS4f3r!s1t"

'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DcsInstancePasswordModule(OTCModule):
    argument_spec = dict(
        id=dict(required=True),
        old_password=dict(required=True, no_log=True),
        new_password=dict(required=True, no_log=True)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        changed = False

        instance = self.conn.dcs.find_instance(
            name_or_id=self.params['id'],
            ignore_missing=True
        )
        if instance:
            if not self.ansible.check_mode:
                dcs_instance = self.conn.dcs.change_instance_password(instance.id, self.params['old_password'], self.params['new_password'])
                self.exit(changed=True, dcs_instance=dcs_instance.to_dict())
            self.exit(True)
        else:
            self.exit(
                changed=False,
                message=('No Instance with name or id %s found!', self.params['id']),
                failed=True
            )


def main():
    module = DcsInstancePasswordModule()
    module()


if __name__ == "__main__":
    main()
