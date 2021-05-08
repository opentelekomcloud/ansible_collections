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
---
module: vpc_peering_mode
short_description: Add/Update/Delete vpc peering connection from OpenTelekomCloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.8.2"
author: "Artem Goncharov (@gtema)"
description:
  - Accept or Reject VPC peering request.
options:
  name:
    description:
      - Name of the vpc peering connection.
    type: str
  mode:
    description:
      - Mode to be used.
    type: str
    choices: ['accept', 'reject']
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
vpc_peering:
  description: Dictionary describing VPC peering instance.
  type: complex
  returned: On Success.
  contains:
    id:
      description: Specifies the VPC peering connection ID.
      returned: On success when C(state=present)
      type: str
      sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
    name:
      description: Specifies the VPC peering connection name.
      returned: On success when C(state=present)
      type: str
      sample: "vpc_peering1"
    status:
      description: Specifies the VPC peering connection status.
      returned: On success when C(state=present)
      type: str
      sample: "accepted"
    request_vpc_info:
      description: Dictionary describing the local vpc.
      returned: On success when C(state=present)
      type: complex
      contains:
        vpc_id:
          description: Specifies the ID of a VPC involved in a VPC peering connection.
          type: str
          sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
        project_id:
          description: Specifies the ID of the project to which a VPC involved in the VPC peering connection belongs.
          type: str
          sample: "45007a7e-ee4f-4d13-8283-b4da2e037c69"
    accept_vpc_info:
      description: Dictionary describing the local vpc.
      returned: On success when C(state=present)
      type: complex
      contains:
        vpc_id:
          description: Specifies the ID of a VPC involved in a VPC peering connection.
          type: str
          sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
        project_id:
          description: Specifies the ID of the project to which a VPC involved in the VPC peering connection belongs.
          type: str
          sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
    description:
      description: Provides supplementary information about the VPC peering connection.
      returned: On success when C(state=present)
      type: str
      sample: ""
    created_at:
      description: Specifies the time (UTC) when the VPC peering connection is created.
      returned: On success when C(state=present)
      type: str
      sample: "2020-09-13T20:38:02"
    updated_at:
      description: Specifies the time (UTC) when the VPC peering connection is updated.
      returned: On success when C(state=present)
      type: str
      sample: "2020-09-13T20:38:02"
'''

EXAMPLES = '''
# Accept vpc peering.
- opentelekomcloud.cloud.vpc_peering_mode:
    cloud: "cloud_b"
    name: "peering1"
    mode: "accept"

# Reject vpc peering.
- opentelekomcloud.cloud.vpc_peering_mode:
    cloud: "cloud_b"
    name: "peering1"
    mode: "reject"
'''


from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class VPCPeeringModeModule(OTCModule):
    argument_spec = dict(
        name=dict(type='str'),
        mode=dict(type='str', choices=['accept', 'reject'])
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        name = self.params['name']

        vpc_peering = self.conn.vpc.find_peering(name_or_id=name, ignore_missing=True)

        if not vpc_peering:
            self.fail_json(msg='Cannot find requested VPC peering')

        if not vpc_peering.status == 'PENDING_ACCEPTANCE':
            self.exit_json(
                changed=False,
                vpc_peering=vpc_peering
            )
        if not self.ansible.check_mode:
            self.conn.vpc.set_peering(vpc_peering, self.params['mode'])
        self.exit_json(
            changed=True,
            vpc_peering=vpc_peering
        )


def main():
    module = VPCPeeringModeModule()
    module()


if __name__ == '__main__':
    main()
