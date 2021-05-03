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
module: dcs_instance
short_description: Manage DCS Instances on Open Telekom Cloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.8.0"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Manage DCS Instances on Open Telekom Cloud
options:
  name:
    description:
      - Specifies the name of the instance
    type: str
  description:
    description:
      - Specifies the description of the instance
    type: str
  id:
    description:
      - ID of the instance. Needed when modifying an instance
    type: str
  engine:
    description:
      - Cache engine
    type: str
    default: Redis
  engine_version:
    description:
      - Cache Engine Version
    type: str
    default: 3.0
  capacity:
    description:
      - Cache capacity in GB
    type: int
  password:
    description:
      - Password of a DCS instance
      - Password must meet following criteria
      - String 8 to 32 chars, different than the old one, at least 3 of the types (Lowercase, Uppercase, Digits, Special)
    type: str
  vpc_id:
    description:
      - VPC ID
    type: str
  security_group_id:
    description:
      - ID of the Security Group where the instance belongs to
    type: str
  subnet_id:
    description:
      - Network ID of the Subnet
    type: str
  available_zones:
    description:
      - ID of the AZ where the cache node resides and which has available ressources.
    type: list
    elements: str
  product_id:
    description:
      - ID of the product that can be created
    type: str
  instance_backup_policy:
    description:
      - Backup policy
    type: dict
  maintain_begin:
    description:
      - Time at which the maintenance time window starts.
      - Format   HH mm ss
      - Must be set in pairs with maintain_end
    type: str
  maintain_end:
    description:
      - Time at which the maintenance time window ends.
      - Format   HH mm ss
      - Must be set in pairs with maintain_begin
    type: str
  redis_config:
    description:
      - If this param is set for modification, only redis_config will be changed
    type: dict
  restart_instance:
    description:
      - Restart the instance. Do nothing else if true
    type: bool
    default: false
  state:
    choices: [present, absent]
    default: present
    description: Instance state
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
dcs_instance:
    description: Dictionary of DCS instance
    returned: changed
    type: dict
    sample: {
        "dcs_instance": {
            "available_zones": [
                "123456786ce4e948da0b97d9a7d62fb"
            ],
            "backup_policy": {
                "backup_policy_id": "12345678-6d67-4b79-a9b8-0ba20b365070",
                "created_at": "2021-03-01T12:43:05.233Z",
                "policy": {
                    "backup_type": "manual",
                    "periodical_backup_plan": {
                        "backup_at": [
                            1,
                            2,
                            3,
                            4
                        ],
                        "begin_at": "00:00-01:00",
                        "period_type": "weekly",
                        "timezone_offset": null
                    },
                    "save_days": 2
                },
                "tenant_id": "12345678a13b49529d2e2c3646691288",
                "updated_at": "2021-03-02T08:59:16.069Z"
            },
            "capacity": 8,
            "charging_mode": 0,
            "created_at": "2021-03-01T12:43:05.245Z",
            "description": "",
            "domain_name": "",
            "engine": "Redis",
            "engine_version": "3.0",
            "error_code": null,
            "id": "12345678-20fb-441b-a0cd-46369a9f7db0",
            "internal_version": null,
            "ip": "192.168.10.177",
            "location": {
                "cloud": "otc",
                "project": {
                    "domain_id": null,
                    "domain_name": null,
                    "id": "12345678a13b49529d2e2c3646691288",
                    "name": "eu-de"
                },
                "region_name": "eu-de",
                "zone": null
            },
            "lock_time": null,
            "lock_time_left": null,
            "maintain_begin": "22:00:00",
            "maintain_end": "02:00:00",
            "max_memory": 6554,
            "message": null,
            "name": "test_dcs",
            "order_id": null,
            "password": null,
            "port": 6379,
            "product_id": "OTC_DCS_MS",
            "resource_spec_code": "dcs.master_standby",
            "result": null,
            "retry_times_left": null,
            "security_group_id": "12345678-b782-4aff-8311-19896597fd4e",
            "security_group_name": "sg-test",
            "status": "RUNNING",
            "subnet_cidr": "192.168.10.0/24",
            "subnet_id": "12345678-ca80-4b49-bbbb-85ea9b96f8b3",
            "subnet_name": "subnet-sebastian",
            "used_memory": 4,
            "user_id": "1234567890bb4c6f81bc358d54693962",
            "user_name": "sgode",
            "vpc_id": "12345678-dc40-4e3a-95b1-5a0756441e12",
            "vpc_name": "vpc-test"
        }
    }
'''

EXAMPLES = '''
# Create DCS Instance
- opentelekomcloud.cloud.dcs_instance:
    name: "dcs_test"
    password: "Thatson3v3rysecureP4ssw0rd"
    capacity: "4"
    vpc_id: 12345678-dc40-4e3a-95b1-5a0756441e12
    security_group_id: 12345678-b782-4aff-8311-19896597fd4e
    subnet_id: 12345678-ca80-4b49-bbbb-85ea9b96f8b3
    available_zones:
        - bf84aba586ce4e948da0b97d9a7d62fb
    product_id: OTC_DCS_MS
    instance_backup_policy:
        save_days: "2"
        backup_type: "manual"
        periodical_backup_plan:
        begin_at: "00:00-01:00"
        period_type: "weekly"
        backup_at:
            - 1
            - 2
            - 3
            - 4
    maintain_begin: "22:00:00"
    maintain_end: "02:00:00"

# Modify DCS Instance
- opentelekomcloud.cloud.dcs_instance:
    name: "dcs_test_2"
    id: 12345678-dc40-4e3a-95b1-5a0756441e12
    description: "Test-description"
    instance_backup_policy:
        save_days: "2"
        backup_type: "manual"
        periodical_backup_plan:
        begin_at: "00:00-01:00"
        period_type: "weekly"
        backup_at:
            - 1
            - 2
            - 3
    maintain_begin: "23:00:00"
    maintain_end: "03:00:00"

# Delete DCS Instance
- opentelekomcloud.cloud.dcs_instance:
    name: "dcs_test_2"
    state: absent
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DcsInstanceModule(OTCModule):
    argument_spec = dict(
        name=dict(required=False),
        id=dict(required=False),
        description=dict(required=False),
        engine=dict(required=False, default='Redis'),
        engine_version=dict(required=False, default='3.0'),
        capacity=dict(required=False, type='int'),
        password=dict(required=False),
        vpc_id=dict(required=False),
        security_group_id=dict(required=False),
        subnet_id=dict(required=False),
        available_zones=dict(required=False, type='list', elements='str'),
        product_id=dict(required=False),
        instance_backup_policy=dict(required=False, type='dict'),
        maintain_begin=dict(required=False),
        maintain_end=dict(required=False),
        redis_config=dict(required=False, type='dict'),
        restart_instance=dict(required=False, type='bool', default='false'),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        changed = False

        if self.params['id']:
            nameid = self.params['id']
        elif self.params['name']:
            nameid = self.params['name']
        else:
            self.exit(
                changed=False,
                message=('No Name or ID provided, but required!'),
                failed=True
            )

        instance = self.conn.dcs.find_instance(
            name_or_id=nameid,
            ignore_missing=True
        )

        # Instance Deletion
        if self.params['state'] == 'absent':
            if instance:
                if self.ansible.check_mode:
                    self.exit(changed=True)
                dcs_instance = self.conn.dcs.delete_instance(instance.id)
                self.exit(changed=True, dcs_instance=dcs_instance)

        if self.params['state'] == 'present':
            attrs = {}
            # Modifying an Instance
            if instance:
                if not self.params['capacity']:
                    capacity_var = -1  # This is done to prevent an error if no capacity has been given
                else:
                    capacity_var = self.params['capacity']
                if self.params['restart_instance'] is True:
                    if self.ansible.check_mode:
                        self.exit(changed=True)
                    dcs_instance = self.conn.dcs.restart_instance(instance.id)
                    self.exit(changed=True, dcs_instance=dcs_instance.to_dict())
                # elif self.params['redis_config']:
                #     attrs['redis_config'] = {
                #         'param_id': self.params['redis_config']['param_id'],
                #         'param_name': self.params['redis_config']['param_name'],
                #         'param_value': self.params['redis_config']['param_value']
                #     }
                #     if self.ansible.check_mode:
                #         self.exit(changed=True)
                #     dcs_instance = self.conn.dcs.update_instance_params(instance.id, **attrs)
                #     self.exit(changed=True, dcs_instance=dcs_instance.to_dict())
                # Scaling up
                elif instance.to_dict()['capacity'] < capacity_var and capacity_var != -1:
                    if self.ansible.check_mode:
                        self.exit(changed=True)
                    dcs_instance = self.conn.dcs.extend_instance(instance.id, self.params['capacity'])
                    self.exit(changed=True, dcs_instance=dcs_instance.to_dict(), message='Scaling instance up, ignoring other params')
                elif instance.to_dict()['capacity'] > capacity_var and capacity_var != -1:
                    self.exit(
                        changed=False,
                        message=('''When extending an DCS Instance the capacity needs to be larger!
                                The Instance has a capacity of %s and new provided capacity was %s'''
                                 % (instance.to_dict()['capacity'], self.params['capacity'])),
                        failed=True
                    )
                # Changing other params
                elif instance.to_dict()['capacity'] == capacity_var or capacity_var == -1:
                    changed = False
                    if instance.to_dict()['name'] != self.params['name']:
                        changed = True
                        attrs['name'] = self.params['name']
                    if instance.to_dict()['description'] != self.params['description']:
                        changed = True
                        attrs['description'] = self.params['description']
                    if instance.to_dict()['security_group_id'] != self.params['security_group_id']:
                        changed = True
                        attrs['security_group_id'] = self.params['security_group_id']
                    if (instance.to_dict()['maintain_begin'] != self.params['maintain_begin']) and \
                       (instance.to_dict()['maintain_end'] != self.params['maintain_end']):
                        changed = True
                        attrs['maintain_begin'] = self.params['maintain_begin']
                        attrs['maintain_end'] = self.params['maintain_end']
                    elif (instance.to_dict()['maintain_begin'] != self.params['maintain_begin']) or \
                         (instance.to_dict()['maintain_end'] != self.params['maintain_end']):
                        self.exit(
                            changed=False,
                            message=('''You need to specify maintain_begin and maintain_end when trying to change one of them'''),
                            failed=True
                        )
                    # The Query API currently will always give a NULL response for backup_policy so this will always result in "changed"
                    # There's no way to go around this
                    if instance.to_dict()['backup_policy'] != self.params['instance_backup_policy']:
                        changed = True
                        instance_backup_policy_var = self.params['instance_backup_policy']
                        # In case the user didn't specify timezone_offset or something we need to give the API an null type so it won't throw an error
                        try:
                            instance_backup_policy_var['periodical_backup_plan']['timezone_offset'] = \
                                (instance_backup_policy_var['periodical_backup_plan']['timezone_offset'])
                        except Exception:
                            instance_backup_policy_var['periodical_backup_plan']['timezone_offset'] = None
                        try:
                            instance_backup_policy_var['save_days'] = (instance_backup_policy_var['save_days'])
                        except Exception:
                            instance_backup_policy_var['save_days'] = None
                        try:
                            instance_backup_policy_var['backup_type'] = (instance_backup_policy_var['backup_type'])
                        except Exception:
                            instance_backup_policy_var['backup_type'] = None

                        attrs['instance_backup_policy'] = {
                            "save_days": instance_backup_policy_var['save_days'],
                            "backup_type": instance_backup_policy_var['backup_type'],
                            "periodical_backup_plan": {
                                "begin_at": instance_backup_policy_var['periodical_backup_plan']['begin_at'],
                                "period_type": instance_backup_policy_var['periodical_backup_plan']['period_type'],
                                "backup_at": instance_backup_policy_var['periodical_backup_plan']['backup_at'],
                                "timezone_offset": instance_backup_policy_var['periodical_backup_plan']['timezone_offset']
                            }
                        }

                    if self.ansible.check_mode:
                        self.exit(changed=True)
                    dcs_instance = self.conn.dcs.update_instance(instance.id, **attrs)
                    self.exit(changed=True, dcs_instance=dcs_instance.to_dict())

            # Creating a new Instance
            if not instance:
                if not self.params['name']:
                    self.exit(
                        changed=False,
                        message=('No name param provided, but required!'),
                        failed=True
                    )
                if self.params['engine']:
                    engine_var = self.params['engine']
                else:
                    self.exit(
                        changed=False,
                        message=('No engine param provided, but required!'),
                        failed=True
                    )
                if self.params['engine_version']:
                    engine_version_var = self.params['engine_version']
                else:
                    self.exit(
                        changed=False,
                        message=('No engine_version param provided, but required!'),
                        failed=True
                    )
                if self.params['capacity']:
                    capacity_var = self.params['capacity']
                else:
                    self.exit(
                        changed=False,
                        message=('No capacity param provided, but required!'),
                        failed=True
                    )
                if self.params['password']:
                    password_var = self.params['password']
                else:
                    self.exit(
                        changed=False,
                        message=('No password param provided, but required!'),
                        failed=True
                    )
                if self.params['vpc_id']:
                    vpc_id_var = self.params['vpc_id']
                else:
                    self.exit(
                        changed=False,
                        message=('No vpc_id param provided, but required!'),
                        failed=True
                    )
                if self.params['security_group_id']:
                    security_group_id_var = self.params['security_group_id']
                else:
                    self.exit(
                        changed=False,
                        message=('No security_group_id param provided, but required!'),
                        failed=True
                    )
                if self.params['subnet_id']:
                    subnet_id_var = self.params['subnet_id']
                else:
                    self.exit(
                        changed=False,
                        message=('No subnet_id param provided, but required!'),
                        failed=True
                    )
                if self.params['available_zones']:
                    available_zones_var = self.params['available_zones']
                else:
                    self.exit(
                        changed=False,
                        message=('No available_zones param provided, but required!'),
                        failed=True
                    )
                if self.params['product_id']:
                    product_id_var = self.params['product_id']
                else:
                    self.exit(
                        changed=False,
                        message=('No product_id param provided, but required!'),
                        failed=True
                    )
                if self.params['maintain_begin'] and self.params['maintain_end']:
                    maintain_begin_var = self.params['maintain_begin']
                    maintain_end_var = self.params['maintain_end']
                else:
                    maintain_begin_var = None
                    maintain_end_var = None

                attrs = {
                    "name": self.params['name'],
                    "description": self.params['description'],
                    "engine": engine_var,
                    "engine_version": engine_version_var,
                    "capacity": capacity_var,
                    "password": password_var,
                    "vpc_id": vpc_id_var,
                    "security_group_id": security_group_id_var,
                    "subnet_id": subnet_id_var,
                    "available_zones": available_zones_var,
                    "product_id": product_id_var,
                    "maintain_begin": maintain_begin_var,
                    "maintain_end": maintain_end_var,
                }
                if self.params['instance_backup_policy']:
                    instance_backup_policy_var = self.params['instance_backup_policy']
                    # In case the user didn't specify timezone_offset or something we need to give the API an null type so it won't throw an error
                    try:
                        instance_backup_policy_var['periodical_backup_plan']['timezone_offset'] = \
                            (instance_backup_policy_var['periodical_backup_plan']['timezone_offset'])
                    except Exception:
                        instance_backup_policy_var['periodical_backup_plan']['timezone_offset'] = None
                    try:
                        instance_backup_policy_var['save_days'] = (instance_backup_policy_var['save_days'])
                    except Exception:
                        instance_backup_policy_var['save_days'] = None
                    try:
                        instance_backup_policy_var['backup_type'] = (instance_backup_policy_var['backup_type'])
                    except Exception:
                        instance_backup_policy_var['backup_type'] = None

                    attrs['instance_backup_policy'] = {
                        "save_days": instance_backup_policy_var['save_days'],
                        "backup_type": instance_backup_policy_var['backup_type'],
                        "periodical_backup_plan": {
                            "begin_at": instance_backup_policy_var['periodical_backup_plan']['begin_at'],
                            "period_type": instance_backup_policy_var['periodical_backup_plan']['period_type'],
                            "backup_at": instance_backup_policy_var['periodical_backup_plan']['backup_at'],
                            "timezone_offset": instance_backup_policy_var['periodical_backup_plan']['timezone_offset']
                        }
                    }
                if self.ansible.check_mode:
                    self.exit(changed=True)
                dcs_instance = self.conn.dcs.create_instance(**attrs)
                self.exit(changed=True, dcs_instance=dcs_instance.to_dict())

        self.exit(
            changed=changed
        )


def main():
    module = DcsInstanceModule()
    module()


if __name__ == "__main__":
    main()
