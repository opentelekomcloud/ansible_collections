# Ansible Collection opentelekomcloud.cloud

Ansible Collections for using with OTC (addition to the native OpenStack
modules)

* ``cloud`` - collection containing additional ansible modules for managing
  OTC specific resources (or modified OpenStack modules in case of behavioral
  differencies)

## Requirements

- otcextension
- openstacksdk (installed via otcextensions)

## Installation

Run the following command to install the collection.

```bash
$ ansible-galaxy collection install opentelekomcloud.cloud
```

> If you need further information to get started, please see section:
> ```Installation on a blank system in a Python virtual environment```

## Get started on a blank system in a Python virtual environment

Installation was tested on Ubuntu 20.04

Install ``python3-venv`` for Python virtual environment:

```bash
$ sudo apt-get install python3-venv
```

Create virtual environment ``ansiblevenv``:

```bash
$ python3 -m venv ansiblevenv
```

Install dependencies for python package [otcextensions](https://github.com/opentelekomcloud/python-otcextensions) which are described in its
[documentation](https://python-otcextensions.readthedocs.io/en/latest/):

```bash
$ sudo apt-get install gcc libssl-dev python3-dev
```

Enable virtual environment ``ansiblevenv``:

```bash
$ source ansiblevenv/bin/activate
```

Install ``wheel``, ``ansible`` and ``otcextensions``:

```bash
(ansiblevenv) $ pip install wheel ansible otcextensions setuptools
```

Install opentelekomcloud.cloud collection from Ansible-Galaxy:

```bash
(ansiblevenv) $ ansible-galaxy collection install opentelekomcloud.cloud
```

Prepare credential file ``clouds.yaml`` and necessary folders to connect to
your cloud:

```bash
(ansiblevenv) $ mkdir -p ~/.config/openstack/
(ansiblevenv) $ touch ~/.config/openstack/clouds.yaml
(ansiblevenv) $ chmod 700 -R ~/.config/
```
 
Paste in the following content with your credentials:

```yaml
# clouds.yaml

clouds:
  otc:
    profile: otc
    auth:
      username: '<USER_NAME>'
      password: '<PASSWORD>'
      project_name: '<eu-de_project>'
      # or project_id: '<123456_PROJECT_ID>'
      user_domain_name: 'OTC00000000001000000xxx'
      # or user_domain_id: '<123456_DOMAIN_ID>'
      auth_url: 'https://iam.eu-de.otc.t-systems.com:443/v3'
    interface: 'public'
    identity_api_version: 3 # !Important
    ak: '<AK_VALUE>' # AK/SK pair for access to OBS
    sk: '<SK_VALUE>'
```

Verify the installation process by creating a sample playbook which invokes
all dependencies:

```bash
(ansiblevenv) $ vim opentelekomcloud.yaml
```

```yaml
# opentelekomcloud.yaml

- hosts: localhost
  tasks:
    - name: Get NAT gateway info
      opentelekomcloud.cloud.nat_gateway_info:
        cloud: otc
      register: gw
  
    - name: debug configs
      debug:
        var: gw.nat_gateways
```
[Here](https://github.com/opentelekomcloud/ansible-collection-cloud/tree/master/examples) you can 
find some [examples](https://github.com/opentelekomcloud/ansible-collection-cloud/tree/master/examples) of using OTC collection. All 
the examples are based on real usecases, and contains some tips and tricks.

Run the playbook to verify the functionality:

```bash
(ansiblevenv) $ ansible-playbook opentelekomcloud.yaml

# output without NAT gateways enabled

PLAY [localhost] ***************************************************************

TASK [Gathering Facts] *********************************************************
ok: [localhost]

TASK [Get NAT gateway info] ****************************************************
ok: [localhost]

TASK [debug configs] ***********************************************************
ok: [localhost] => {
    "gw.nat_gateways": []
}
```

## For Developers: additional steps

Create a path where you place your development files e.g.:

```bash
mkdir -p ~/ansible/ansible_collections/opentelekomcloud/
```

Clone the development files into your path and rename it to cloud.

```bash
cd ~/ansible/ansible_collections/opentelekomcloud/
git clone git@github.com:opentelekomcloud/ansible-collection-cloud.git cloud
```

Export the path variable and make it available for your system:

```bash
pwd
> /path/to/your/ansible/ansible_collections/
export ANSIBLE_COLLECTIONS_PATHS=/path/to/your/ansible/ansible_collections/
```

Validate the entry of your development environment by running the following command.

```bash
source ~/youransiblevenv/bin/activate
ansible-galaxy collection list
```
