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
module: dcs_instance_backup
short_description: Manage DCS Instance-Backups on Open Telekom Cloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.8.0"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Manage DCS Instance-Backups on Open Telekom Cloud
options:
  instance_id:
    description:
      - Specifies the name or ID of the instance
    type: str
    required: true
  description:
    description:
      - Specifies the description of the backup
    type: str
  backup_id:
    description:
      - Specifies the backup ID which is required for restoring or deletion
    type: str
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
            "created_at": null,
            "description": null,
            "error_code": null,
            "id": "12345678-4b3a-4dfa-9f13-33c732a8f497",
            "is_restorable": null,
            "location": {
                "cloud": "otc",
                "project": {
                    "domain_id": null,
                    "domain_name": null,
                    "id": "123456768a13b49529d2e2c3646691288",
                    "name": "eu-de"
                },
                "region_name": "eu-de",
                "zone": null
            },
            "name": null,
            "period": null,
            "progress": null,
            "size": null,
            "status": null,
            "type": null,
            "updated_at": null
        }
    }
'''

EXAMPLES = '''
# Create a Backup
- opentelekomcloud.cloud.dcs_instance_backup:
    instance_id: 12345678-20fb-441b-a0cd-46369a9f7db0
    description: "This is a test"

# Restore a backup
- opentelekomcloud.cloud.dcs_instance_backup:
    instance_id: 12345678-20fb-441b-a0cd-46369a9f7db0
    backup_id: 12345678-f021-417f-b019-dc02182926a9

# Delete a backup
- opentelekomcloud.cloud.dcs_instance_backup:
    instance_id: 12345678-20fb-441b-a0cd-46369a9f7db0
    backup_id: 12345678-f021-417f-b019-dc02182926a9
    state: absent
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DcsInstanceModule(OTCModule):
    argument_spec = dict(
        instance_id=dict(required=True),
        description=dict(required=False),
        backup_id=dict(required=False),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        changed = False
        attrs = {}

        instance = self.conn.dcs.find_instance(
            name_or_id=self.params['instance_id'],
            ignore_missing=True
        )
        if instance:
            if self.params['state'] == 'present':
                if self.params['description']:
                    attrs['description'] = self.params['description']
                # Restore Backup
                if self.params['backup_id']:
                    attrs['backup_id'] = self.params['backup_id']
                    if not self.ansible.check_mode:
                        dcs_instance = self.conn.dcs.restore_instance(instance.id, **attrs)
                        self.exit(changed=True, dcs_instance=dcs_instance.to_dict())
                    self.exit_json(True)

                # Create Backup
                else:
                    if not self.ansible.check_mode:
                        dcs_instance = self.conn.dcs.backup_instance(instance.id, **attrs)
                        self.exit(changed=True, dcs_instance=dcs_instance.to_dict())
                    self.exit_json(True)                    

            elif self.params['state'] == 'absent':
                if self.params['backup_id']:
                    if not self.ansible.check_mode:
                        dcs_instance = self.conn.dcs.delete_instance_backup(self.params['backup_id'], instance.id)
                        self.exit(changed=True, dcs_instance=dcs_instance)
                    self.exit_json(True)
                else:
                    self.exit(
                        changed=False,
                        message=('No backup_id %s provided but required for deletion!'),
                        failed=True
                    )

        else:
            self.exit(
                changed=False,
                message=('No Instance with name or id %s found!', self.params['id']),
                failed=True
            )

        self.exit(
            changed=changed
        )


def main():
    module = DcsInstanceModule()
    module()


if __name__ == "__main__":
    main()
