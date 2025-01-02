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
module: nat_gateway
short_description: Manage NAT gateway instances
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.1"
author: "Tino Schreiber (@tischrei)"
description:
  - Manage NAT gateway instances
options:
  admin_state_up:
    description:
      - NAT gateway state.
    type: bool
  description:
    description:
      - Description of the NAT gateway
    type: str
  internal_network:
    description:
      - Name or ID of the network where the NAT gateway is attached to.
      - Mandatory for creating gateway instance.
    type: str
  name:
    description:
      - Name of the NAT gateway.
    type: str
    required: true
  project:
    description:
      - ID or name of the project where the NAT gateway is attached to.
    type: str
  router:
    description:
      - ID or name of the router where the NAT gateway is attached.
      - Mandatory for creating gateway instance.
    type: str
  spec:
    description:
      - Specifies the type of the NAT gateway. 1 (small 10.000 connections),
        2 (medium 50.000 connections), 3 (large 200.000 connections), 4
        (extra-large 1.000.000 connections)
    type: str
    default: "1"
    choices: ["1", "2", "3", "4"]
  state:
    choices: [present, absent]
    default: present
    description: Instance state
    type: str

requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
gateway:
    description: List of dictionaries describing NAT gateways.
    type: complex
    returned: On Success.
    contains:
        admin_state_up:
            description: Specifies whether gateway is up or down.
            type: bool
            sample: True
        created_at:
            description: Creation time of the NAT gateway
            type: str
            sample: "yyyy-mm-dd hh:mm:ss"
        description:
            description: Description of the NAT gateway
            type: str
            sample: "My Gateway"
        id:
            description: ID of the NAT gateway
            type: str
            sample: "my-gateway"
        internal_network_id:
            description: Network ID where the NAT gateway is attached to.
            type: str
            sample: "25d24fc8-d019-4a34-9fff-0a09fde6a123"
        name:
            description: Name of the NAT gateway.
            type: str
            sample: "my-gateway"
        project_id:
            description: Project ID where the NAT gateway is located in.
            type: str
            sample: "25d24fc8-d019-4a34-9fff-0a09fde6a567"
        router_id:
            description: VPC / Router ID where the NAT gateway is attached to.
            type: str
            sample: "25d24fc8-d019-4a34-9fff-0a09fde6a123"
        spec:
            description: Specifies the type of the NAT gateway.
            type: str
            sample: "1"
        status:
            description: Specifies the status of the NAT gateway.
            type: str
            sample: "ACTIVE"
'''

EXAMPLES = '''
# Get configs versions.
- nat_gateway:
    internal_network: 1234f0c7-82e3-478d-8433-dc5984859e3b
    name: my_gateway
    router: 1234f70c-6d1d-471e-a911-6924b7ec6ea9
    state: present
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class NATGatewayModule(OTCModule):
    argument_spec = dict(
        admin_state_up=dict(required=False, type='bool'),
        description=dict(required=False),
        internal_network=dict(required=False),
        name=dict(required=True),
        project=dict(required=False),
        router=dict(required=False),
        spec=dict(required=False, default='1', choices=["1", "2", "3", "4"]),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def _system_state_change(self, obj):
        state = self.params['state']
        if state == 'present':
            if not obj:
                return True
        elif state == 'absent' and obj:
            return True
        return False

    def run(self):
        name = self.params['name']

        changed = False

        gateway = self.conn.nat.find_gateway(
            name_or_id=name,
            ignore_missing=True)

        # Gateway deletion
        if self.params['state'] == 'absent':
            changed = False
            if self.ansible.check_mode:
                self.exit(changed=True)
            if gateway:
                self.conn.nat.delete_gateway(gateway)
                changed = True

        # Gateway creation
        elif self.params['state'] == 'present':
            attrs = {}

            # Gateway already exists
            if gateway:
                # Modify existing gateway
                if ((gateway.description != self.params['description'])
                        and (self.params['description'] is not None)):
                    attrs['description'] = self.params['description']
                if gateway.spec != self.params['spec']:
                    attrs['spec'] = self.params['spec']

                # Specs which cannot be modified and playbook fails if
                # a change is requested
                if self.params['internal_network']:
                    nw = self.conn.network.find_network(
                        name_or_id=self.params['internal_network'],
                        ignore_missing=True)
                    if not nw or nw.id != gateway.internal_network_id:
                        self.exit(
                            changed=False,
                            message=('Existing NAT gateway has different '
                                     'network than %s or network does not '
                                     'exist. The gateway cannot be modified. '
                                     'Please delete existing NAT gateway, '
                                     'first to change the network.'
                                     % self.params['internal_network']),
                            failed=True
                        )
                if self.params['project']:
                    pj = self.conn.identity.find_project(
                        name_or_id=self.params['project'],
                        ignore_missing=True)
                    if not pj or pj.id != gateway.project_id:
                        self.exit(
                            changed=False,
                            message=('Existing NAT gateway has different '
                                     'project than %s or project does not '
                                     'exist. The gateway cannot be modified. '
                                     'Please delete existing NAT gateway, '
                                     'first to change the project.'
                                     % self.params['project']),
                            failed=True
                        )
                if self.params['router']:
                    rt = self.conn.network.find_router(
                        name_or_id=self.params['router'],
                        ignore_missing=True)
                    if not rt or rt.id != gateway.router_id:
                        self.exit(
                            changed=False,
                            message=('Existing NAT gateway has different '
                                     'router than %s or router does not '
                                     'exist. The gateway cannot be modified. '
                                     'Please delete existing NAT gateway, '
                                     'first to change the router.'
                                     % self.params['router']),
                            failed=True
                        )
                if attrs:
                    if self.ansible.check_mode:
                        self.exit(changed=True)
                    gateway = self.conn.nat.update_gateway(
                        gateway=gateway,
                        **attrs)
                    self.exit(changed=True, gateway=gateway.to_dict())
                # Gateway with same specs exists
                if self.ansible.check_mode:
                    self.exit(changed=False)
                self.exit(changed=False, gateway=gateway.to_dict())

            # New gateway creatioon
            if self.params['admin_state_up']:
                attrs['admin_state_up'] = self.params['admin_state_up']
            if self.params['description']:
                attrs['description'] = self.params['description']

            nw = self.conn.network.find_network(
                name_or_id=self.params['internal_network'],
                ignore_missing=True)
            if nw:
                attrs['internal_network_id'] = nw.id
            else:
                self.exit(
                    changed=False,
                    snat_rules=[],
                    message=('No network found with name or id: %s' %
                             self.params['internal_network']),
                    failed=True
                )

            attrs['name'] = self.params['name']
            if self.params['project']:
                attrs['project_id'] = self.params['project']

            rt = self.conn.network.find_router(
                name_or_id=self.params['router'],
                ignore_missing=True)
            if rt:
                attrs['router_id'] = rt.id
            else:
                self.exit(
                    changed=False,
                    message=('No router found with name or id: %s' %
                             self.params['router']),
                    failed=True
                )

            if self.params['spec']:
                attrs['spec'] = self.params['spec']
            if self.ansible.check_mode:
                self.exit(changed=True)
            gateway = self.conn.nat.create_gateway(**attrs)
            self.exit(changed=True, gateway=gateway.to_dict())

        self.exit(changed=changed)


def main():
    module = NATGatewayModule()
    module()


if __name__ == "__main__":
    main()
