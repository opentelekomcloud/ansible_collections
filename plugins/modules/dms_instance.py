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
module: dms_instance
short_description: Manage DMS Instances on Open Telekom Cloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.1.2"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Manage DMS Instances on Open Telekom Cloud
options:
  name:
    description:
      - Name of the Instance. Can also be ID for deletion.
    type: str
    required: true
  description:
    description:
      - Description.
    type: str
  engine:
    description:
      - Indicates a message engine.
      - Required for creation.
    type: str
    default: kafka
  engine_version:
    description:
      - Indicates the version of the message engine.
      - Required for creation.
    type: str
    default: 2.3.0
  storage_space:
    description:
      - Indicates the message storage space with increments of 100 GB.
      - Required for creation
    type: int
  access_user:
    description:
      - Indicates a username.
      - Required when ssl_enable is true.
    type: str
  password:
    description:
      - Indicates the instance password.
      - Required when ssl_enable is true.
    type: str
  vpc_id:
    description:
      - Indicates VPC ID.
      - Required for creation
    type: str
  security_group_id:
    description:
      - Indicates Security Group ID.
      - Required for creation
    type: str
  subnet_id:
    description:
      - Indicates Network ID.
      - Required for creation
    type: str
  available_zones:
    description:
      - Indicates ID of an AZ.
      - Required for creation
    type: list
    elements: str
  product_id:
    description:
      - Indicates Product ID.
      - Required for creation
    type: str
  maintain_begin:
    description:
      - Indicates Beginning of mantenance time window.
      - Must be set in pairs with maintain_end
    type: str
  maintain_end:
    description:
      - Indicates End of maintenance Window.
      - Must be set in pairs with maintain_begin
    type: str
  ssl_enable:
    description:
      - Indicates whether to enable SSL-encrypted access to the Instance.
    type: bool
    default: False
  enable_publicip:
    description:
      - Indicates whether to enable ppublic access to the instance.
    type: bool
  public_bandwidth:
    description:
      - Indicates the public network bandwidth.
    type: str
  retention_policy:
    description:
      - Indicates the action to be taken when the memory usage reaches the disk capacity threshold.
    type: str
  storage_spec_code:
    description:
      - Indicates I/O specification of a Kafka instance.
      - Required for creation
    type: str
  state:
    choices: [present, absent]
    default: present
    description: Instance state
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
instance:
    description: Dictionary of Instance
    returned: changed
    type: dict
    sample: {
        "instance": {
            "access_user": null,
            "availability_zones": [
                "eu-de-03"
            ],
            "charging_mode": null,
            "connect_address": null,
            "created_at": null,
            "description": null,
            "engine_name": "kafka",
            "engine_version": "2.3.0",
            "id": "12345678-e7c4-4ba1-8aa2-f2c4eb507c43",
            "instance_id": "12345678-e7c4-4ba1-8aa2-f2c4eb507c43",
            "is_public": null,
            "is_ssl": null,
            "kafka_public_status": null,
            "location": {
                "cloud": "otc",
                "project": {
                    "domain_id": null,
                    "domain_name": null,
                    "id": "1234",
                    "name": "eu-de"
                },
                "region_name": "eu-de",
                "zone": null
            },
            "maintenance_end": null,
            "maintenance_start": null,
            "max_partitions": null,
            "name": "aed93756fa3c04e4083c5b48ad6ba6258-instance",
            "network_id": "12345678-ca80-4b49-bbbb-85ea9b96f8b3",
            "password": null,
            "port": null,
            "product_id": "00300-30308-0--0",
            "public_bandwidth": null,
            "retention_policy": null,
            "router_id": "12345678-dc40-4e3a-95b1-5a0756441e12",
            "router_name": null,
            "security_group_id": "12345678-9b1f-4af8-9b53-527ff05c5e12",
            "security_group_name": null,
            "service_type": null,
            "spec": null,
            "spec_code": null,
            "status": null,
            "storage": 600,
            "storage_resource_id": null,
            "storage_spec_code": "dms.physical.storage.ultra",
            "storage_type": null,
            "total_storage": null,
            "type": null,
            "used_storage": null,
            "user_id": null,
            "user_name": null
        }
    }
'''

EXAMPLES = '''
# Create Kafka Instance
- opentelekomcloud.cloud.dms_instance:
    name: 'test'
    storage_space: '600'
    vpc_id: '12345678-dc40-4e3a-95b1-5a0756441e12'
    security_group_id: '12345678'
    subnet_id: '12345678-ca80-4b49-bbbb-85ea9b96f8b3'
    available_zones: ['eu-de-03']
    product_id: '00300-30308-0--0'
    storage_spec_code: 'dms.physical.storage.ultra'

# Delete Kafka Instance
- opentelekomcloud.cloud.dms_instance:
    name: 'kafka-c76z'
    state: absent

# Update Kafka Instance
- opentelekomcloud.cloud.dms_instance:
    name: 'kafka-s1dd'
    description: 'Test'
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DmsInstanceModule(OTCModule):
    argument_spec = dict(
        name=dict(required=True),
        description=dict(required=False),
        engine=dict(required=False, default='kafka'),
        engine_version=dict(required=False, default='2.3.0'),
        storage_space=dict(required=False, type='int'),
        access_user=dict(required=False),
        password=dict(required=False),
        vpc_id=dict(required=False),
        security_group_id=dict(required=False),
        subnet_id=dict(required=False),
        product_id=dict(required=False),
        available_zones=dict(required=False, type='list', elements='str'),
        maintain_begin=dict(required=False),
        maintain_end=dict(required=False),
        ssl_enable=dict(required=False, type='bool', default='False'),
        enable_publicip=dict(required=False, type='bool'),
        public_bandwidth=dict(required=False),
        retention_policy=dict(required=False),
        storage_spec_code=dict(required=False),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        attrs = {}
        instance = self.conn.dms.find_instance(name_or_id=self.params['name'], ignore_missing=True)

        attrs['name'] = self.params['name']
        if self.params['description']:
            attrs['description'] = self.params['description']
        if self.params['maintain_begin'] and self.params['maintain_end']:
            attrs['maintain_begin'] = self.params['maintain_begin']
            attrs['maintain_end'] = self.params['maintain_end']
        elif self.params['maintain_end'] or self.params['maintain_begin']:
            self.exit(
                changed=False,
                failed=True,
                message=('Both maintain_end and maintain_begin need to be defined.')
            )

        if self.params['state'] == 'present':

            # Instance creation
            if not instance:

                if self.params['engine']:
                    attrs['engine'] = self.params['engine']
                else:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('No engine param provided')
                    )
                if self.params['engine_version']:
                    attrs['engine_version'] = self.params['engine_version']
                else:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('No engine_version param provided')
                    )
                if self.params['storage_space']:
                    attrs['storage_space'] = self.params['storage_space']
                else:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('No storage_space param provided')
                    )
                if self.params['access_user'] and self.params['ssl_enable'] is True:
                    attrs['access_user'] = self.params['access_user']
                elif self.params['access_user'] and self.params['ssl_enable'] is False:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('access_user specified but ssl_enable is false')
                    )
                if self.params['password'] and self.params['ssl_enable'] is True:
                    attrs['password'] = self.params['password']
                elif self.params['password'] and self.params['ssl_enable'] is False:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('Password specified but ssl_enable is false')
                    )
                if self.params['vpc_id']:
                    attrs['vpc_id'] = self.params['vpc_id']
                else:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('No vpc_id param provided')
                    )
                if self.params['security_group_id']:
                    attrs['security_group_id'] = self.params['security_group_id']
                else:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('No security_group_id param provided')
                    )
                if self.params['subnet_id']:
                    attrs['subnet_id'] = self.params['subnet_id']
                else:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('No subnet_id param provided')
                    )
                if self.params['available_zones']:
                    attrs['available_zones'] = self.params['available_zones']
                else:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('No available_zones param provided')
                    )
                if self.params['product_id']:
                    attrs['product_id'] = self.params['product_id']
                else:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('No product_id param provided')
                    )
                if self.params['ssl_enable'] is True and self.params['password']:
                    attrs['ssl_enable'] = self.params['ssl_enable']
                elif self.params['ssl_enable'] is True and not self.params['password']:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('ssl_enable is true, but no password defined')
                    )
                if self.params['enable_publicip']:
                    attrs['enable_publicip'] = self.params['enable_publicip']
                if self.params['public_bandwidth']:
                    attrs['public_bandwidth'] = self.params['public_bandwidth']
                if self.params['retention_policy']:
                    attrs['retention_policy'] = self.params['retention_policy']
                if self.params['storage_spec_code']:
                    attrs['storage_spec_code'] = self.params['storage_spec_code']
                else:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('No storage_spec_code param provided')
                    )

                if self.ansible.check_mode:
                    self.exit(changed=True)
                instance = self.conn.dms.create_instance(**attrs)
                self.exit(changed=True, instance=instance.to_dict())

            # Instance Modification
            elif instance:
                if self.params['security_group_id']:
                    attrs['security_group_id'] = self.params['security_group_id']

                if self.ansible.check_mode:
                    self.exit(changed=True)
                instance = self.conn.dms.update_instance(instance, **attrs)
                self.exit(changed=True, instance=instance.to_dict())

        if self.params['state'] == 'absent':

            # Instance Deletion
            if instance:
                if self.ansible.check_mode:
                    self.exit(changed=True)
                instance = self.conn.dms.delete_instance(instance)
                self.exit(changed=True, instance=instance)

            elif not instance:
                self.exit(
                    changed=False,
                    failed=True,
                    message=('No Instance with name or ID %s found') % (self.params['name'])
                )


def main():
    module = DmsInstanceModule()
    module()


if __name__ == "__main__":
    main()
