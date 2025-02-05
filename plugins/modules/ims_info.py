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
module: ims_info
short_description: Get info about images.
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.12.5"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Get image informations from the OTC.
options:
  name:
    description:
      - name or ID of the image to be queried.
    type: str
  isregistered:
    description:
      - Specifies whether the image is available.
    type: bool
  imagetype:
    description:
      - Specifies the image type.
    type: str
    choices: ['gold', 'private', 'shared']
  whole_image:
    description:
      - Specifies whether the image is a full-ECS image.
    type: bool
  system_cmkid:
    description:
      - Specifies the ID of the key used to encrypt the image.
    type: str
  protected:
    description:
      - Specifies whether the image is protected.
    type: bool
  visibility:
    description:
      - Specifies whether the image is available to other tenants.
    type: str
    choices: ['public', 'private', 'shared']
  owner:
    description:
      - Specifies the tenant to which the image belongs.
    type: str
  status:
    description:
      - Specifies the image status.
    type: str
    choices: ['queued', 'saving', 'deleted', 'killed', 'active']
  container_format:
    description:
      - Specifies the container type.
    type: str
    choices: ['bare']
  disk_format:
    description:
      - Specifies the image format. 
    type: str
    choices: ['zvhd2', 'vhd', 'zvhd', 'raw', 'qcow2']
  min_ram:
    description:
      - Specifies the minimum memory size (MB) required for running the image. 
    type: int
  min_disk:
    description:
      - Specifies the minimum disk space (GB) required for running the image.
    type: int
  os_bit:
    description:
      - Specifies the OS architecture, 32 bit or 64 bit.
    type: str
    choices: ['32', '64']
  platform:
    description:
      - Specifies the image platform type.
    type: str
    choices: ['Windows', 'Ubuntu', 'Red Hat', 'SUSE', 'CentOS', 'Debian', 'OpenSUSE', 'Oracle Linux', 'Fedora', 'CoreOS', 'EulerOS', 'Other']
  marker:
    description:
      - Specifies the start number from which images are queried. The value is the image ID.
    type: str
  os_type:
    description:
      - Specifies the image OS type.
    type: str
    choices: ['Linux', 'Windows', 'Other']
  tag:
    description:
      - Specifies a tag added to an image.
    type: str
  member_status:
    description:
      - Specifies the member status. Visibility must be set to "shared" during the query.
    type: str
    choices: ['accepted', 'rejected', 'pending']
  support_kvm:
    description:
      - Specifies whether the image supports KVM.
    type: bool
  support_xen:
    description:
      - Specifies whether the image supports Xen.
    type: bool
  support_largememory:
    description:
      - Specifies whether the image supports large-memory ECSs.
    type: bool
  support_diskintensive:
    description:
      - Specifies whether the image supports disk-intensive ECSs.
    type: bool
  support_highperformance:
    description:
      - Specifies whether the image supports high-performance ECSs.
    type: bool
  support_xen_gpu_type:
    description:
      - Specifies whether the image supports GPU-accelerated ECSs on the KVM platform. This attribute cannot co-exist with support_xen and support_kvm.
    type: bool
  support_kvm_gpu_type:
    description:
      - Specifies whether the image supports GPU-accelerated ECSs on the KVM platform. This attribute cannot co-exist with support_xen and support_kvm.
    type: bool
  support_xen_hana:
    description:
      - Specifies whether the image supports HANA ECSs on the Xen platform. This attribute cannot co-exist with support_xen and support_kvm.
    type: bool
  support_kvm_infiniband:
    description:
      - Specifies whether the image supports ECSs with InfiniBand NICs on the KVM platform. This attribute cannot co-exist with support_xen.
    type: bool
  virtual_env_type:
    description:
      - Specifies the environment where the image is used.
    type: str
    choices: ['FusionCompute', 'Ironic', 'DataImage', 'IsoImage']
  enterprise_project_id:
    description:
      - Specifies the enterprise project to which the images to be queried belong.
    type: str
  
  
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
keys:
    description:
        - Info about about a image.
    returned: On Success
    type: complex
    contains:
        file:
          description: Specifies the URL for uploading and downloading the image file.
          type: str
          sample: "/v2/images/bc6bed6e-ba3a-4447-afcc-449174a3eb52/file"
        owner:
          description: Specifies the tenant to which the image belongs.
          type: str
          sample: "1bed856811654c1cb661a6ca845ebc77"
        id:
          description: Specifies the image ID.
          type: str
          sample: "bc6bed6e-ba3a-4447-afcc-449174a3eb52"
        self:
          description: Specifies the image URL.
          type: str
          sample: "/v2/images/bc6bed6e-ba3a-4447-afcc-449174a3eb52"
        schema:
          description: Specifies the image schema.
          type: str
          sample: "/v2/schemas/image"
        status:
          description:Specifies the image status.
          type: str
          sample: "active"
        tags:
          description: Specifies tags of the image.
          type: list
        visibility:
          description: Specifies whether the image is available to other tenants.
          type: str
          sample: "public"
        name:
          description: Specifies the image name.
          type: str
          sample: "image1"
        protected:
          description: Specifies whether the image is protected. 
          type: bool
        container_format:
          description: Specifies the container type.
          type: str
          sample: "bare"
        min_ram:
          description: Specifies the minimum memory size (MB) required for running the image.
          type: int
          sample: 2048
        max_ram:
          description: Specifies the maximum memory (MB) of the image.
          type: str
          sample: "2048"
        updated_at:
          description: Specifies the time when the image was updated. The value is in UTC format.
          type: str
          sample: "2018-09-06T15:17:33Z"
        __os_bit:
          description: Specifies the OS architecture, 32 bit or 64 bit.
          type: str
          sample: "64"
        __os_version:
          description: Specifies the OS version.
          type: str
          sample: "CentOS 7.3 64bit"
        __description:
          description: Provides supplementary information about the image.
          type: str
        disk_format:
          description: Specifies the image format.
          type: str
          sample: "zvhd2"
        __isregistered:
          description: Specifies whether the image has been registered.
          type: str
          sample: "true"
        __platform:
          description: Specifies the image platform type. 
          type: str
          sample: "Windows"
        __os_type:
          description: Specifies the OS type.
          type: str
          sample: "Linux"
        min_disk:
          description: Specifies the minimum disk space (GB) required for running the image.
          type: int
          sample: "40"
        virtual_env_type:
          description: Specifies the environment where the image is used.
          type: str
          sample: "Ironic"
        __image_source_type:
          description: Specifies the image backend storage type.
          type: str
          sample: "UDS"
        __imagetype:
          description: Specifies the image type.
          type: str
          sample: "Gold"
        created_at:
          description: Specifies the time when the image was created. The value is in UTC format.
          type: str
          sample: "2018-09-06T15:17:33Z"
        __originalimagename:
          description: Specifies the parent image ID.
          type: str
        __backup_id:
          description: Specifies the backup ID.
          type: str
        __image_size:
          description: Specifies the size (bytes) of the image file.
          type: str
          sample: "2000000"
        __data_origin:
          description: Specifies the image source.
          type: str
        __lazyloading:
          description: Specifies whether the image supports lazy loading.
          type: str
          sample: "false"
        active_at:
          description: Specifies the time when the image status became active.
          type: str
          sample: "2018-09-06T15:17:33Z"
        __os_feature_list:
          description: Specifies additional attributes of the image.
          type: str
        __support_kvm:
          description: Specifies whether the image supports KVM. 
          type: str
          sample: "true"
        __support_xen:
          description: Specifies whether the image supports Xen.
          type: str
          sample: "true"
        __support_largememory:
          description: Specifies whether the image supports large-memory ECSs.
          type: str
          sample: "true"
        __support_diskintensive:
          description: Specifies whether the image supports disk-intensive ECSs.
          type: str
          sample: "true"
        __support_highperformance:
          description: Specifies whether the image supports high-performance ECSs.
          type: str
          sample: "true"
        __support_xen_gpu_type:
          description: Specifies whether the image supports GPU-accelerated ECSs on the Xen platform.
          type: str
          sample: "true"
        __support_kvm_gpu_type:
          description: Specifies whether the image supports GPU-accelerated ECSs on the KVM platform. 
          type: str
          sample: "true"
        __support_xen_hana:
          description: Specifies whether the image supports HANA ECSs on the Xen platform. 
          type: str
          sample: "true"
        __support_kvm_infiniband:
          description: Specifies whether the image supports ECSs with InfiniBand NICs on the KVM platform.
          type: str
          sample: "true"
        enterprise_project_id:
          description: Specifies the enterprise project that the image belongs to.
          type: str
          sample: "0"
        __root_origin:
          description: Specifies that the image is created from an external image file.
          type: str
        __sequence_num:
          description: Specifies the ECS system disk slot number of the image.
          type: str
          sample: "0"
        __support_fc_inject:
          description: Specifies whether the image supports password/private key injection using Cloud-Init.
          type: str
          sample: "true"
        hw_firmware_type:
          description: Specifies the ECS boot mode.
          type: str
          sample: "uefi"
        hw_vif_multiqueue_enabled:
          description: Specifies whether the image supports NIC multi-queue.
          type: str
          sample: "true"
        __system__cmkid:
          description: Specifies the ID of the key used to encrypt the image.
          type: str
        __support_amd:
          description: Specifies whether the image uses AMD's x86 architecture.
          type: str
          sample: "true"
'''

EXAMPLES = '''
# Get info about KMS keys
- opentelekomcloud.cloud.kms_info:
    name: "kms-test-123"
  register: result
'''

import re
from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule

UUID_PATTERN = re.compile(r'^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$', re.IGNORECASE)


class KMSInfoModule(OTCModule):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        isregistered=dict(required=False, type='bool'),
        imagetype=dict(required=False, type='str', choices=['gold', 'private', 'shared']),
        whole_image=dict(required=False, type='bool'),
        system_cmkid=dict(required=False, type='str'),
        protected=dict(required=False, type='bool'),
        visibility=dict(required=False, type='str', choices=['public', 'private', 'shared']),
        owner=dict(required=False, type='str'),
        status=dict(required=False, type='str', choices=['queued', 'saving', 'deleted', 'killed', 'active']),
        container_format=dict(required=False, type='str', choices=['bare']),
        disk_format=dict(required=False, type='str', choices=['zvhd2', 'vhd', 'zvhd', 'raw', 'qcow2']),
        min_ram=dict(required=False, type='int'),
        min_disk=dict(required=False, type='int'),
        os_bit=dict(required=False, type='str', choices=['32', '64']),
        platform=dict(required=False, type='str', choices=['Windows', 'Ubuntu', 'Red Hat', 'SUSE', 'CentOS', 'Debian', 'OpenSUSE', 'Oracle Linux', 'Fedora', 'CoreOS', 'EulerOS', 'Other']),
        marker=dict(required=False, type='str'),
        os_type=dict(required=False, type='str', choices=['Linux', 'Windows', 'Other']),
        tag=dict(required=False, type='str'),
        member_status=dict(required=False, type='str', choices=['accepted', 'rejected', 'pending']),
        support_kvm=dict(required=False, type='bool'),
        support_xen=dict(required=False, type='bool'),
        support_largememory=dict(required=False, type='bool'),
        support_diskintensive=dict(required=False, type='bool'),
        support_highperformance=dict(required=False, type='bool'),
        support_xen_gpu_type=dict(required=False, type='bool'),
        support_kvm_gpu_type=dict(required=False, type='bool'),
        support_xen_hana=dict(required=False, type='bool'),
        support_kvm_infiniband=dict(required=False, type='bool'),
        virtual_env_type=dict(required=False, type='str', choices=['FusionCompute', 'Ironic', 'DataImage', 'IsoImage']),
        enterprise_project_id=dict(required=False, type='str')
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    otce_min_version = '0.31.14'

    def run(self):

        data = []
        query = {}

        if self.params['name'] and self.params['id']:
            self.fail_json(msg="Only specify either name or id, not both.")

        if self.params['name']:
            query['name'] = self.params['name']
        if self.params['imagetype']:
            query['imagetype'] = self.params['imagetype']
        if self.params['system_cmkid']:
            query['system_cmkid'] = self.params['system_cmkid']
        if self.params['visibility']:
            query['visibility'] = self.params['visibility']
        if self.params['owner']:
            query['owner'] = self.params['owner']
        if self.params['platform']:
            query['platform'] = self.params['platform']
        if self.params['os_type']:
            query['os_type'] = self.params['os_type']
        if self.params['tag']:
            query['tag'] = self.params['tag']
        if self.params['virtual_env_type']:
            query['virtual_env_type'] = self.params['virtual_env_type']
        if self.params.get('isregistered', False):
            query['isregistered'] = self.params['isregistered']
        if self.params.get('whole_image', False):
            query['whole_image'] = self.params['whole_image']
        if self.params.get('protected', False):
            query['protected'] = self.params['protected']
        if self.params.get('support_kvm', False):
            query['support_kvm'] = self.params['support_kvm']
        if self.params.get('support_xen', False):
            query['support_xen'] = self.params['support_xen']
        if self.params.get('support_largememory', False):
            query['support_largememory'] = self.params['support_largememory']
        if self.params.get('support_diskintensive', False):
            query['support_diskintensive'] = self.params['support_diskintensive']
        if self.params.get('support_highperformance', False):
            query['support_highperformance'] = self.params['support_highperformance']
        if self.params.get('support_xen_gpu_type', False):
            query['support_xen_gpu_type'] = self.params['support_xen_gpu_type']
        if self.params.get('support_kvm_gpu_type', False):
            query['support_kvm_gpu_type'] = self.params['support_kvm_gpu_type']
        if self.params.get('support_xen_hana', False):
            query['support_xen_hana'] = self.params['support_xen_hana']
        if self.params.get('support_kvm_infiniband', False):
            query['support_kvm_infiniband'] = self.params['support_kvm_infiniband']
        if self.params.get('min_ram'):
            query['min_ram'] = self.params['min_ram']
        if self.params.get('min_disk'):
            query['min_disk'] = self.params['min_disk']
        if self.params['os_bit']:
            query['os_bit'] = self.params['os_bit']
        if self.params['enterprise_project_id']:
            query['enterprise_project_id'] = self.params['enterprise_project_id']

        else:
            for raw in self.conn.ims.keys(**query):
                dt = raw.to_dict()
                dt.pop('location')
                data.append(dt)

        self.exit(
            changed=False,
            keys=data
        )


def main():
    module = KMSInfoModule()
    module()


if __name__ == '__main__':
    main()
