# Oracle DBaaS Collection

Oracle dbaas `oracle.dbaas` Ansible Collection provides an easy way to provision and manage resources in Oracle Cloud and on-premises using Ansible.

<!--start requires_ansible-->
<!--end requires_ansible-->

## Installation

### Create a new Python virtual environment

Ansible is based on Python and leverages many Python modules and plugins. When you test something new, it could require you to update a module that your Ansible installation depends on. Upgrading a component that your production environment depends on defeats the purpose of testing. Still, you can have different versions of Ansible and other important Python modules in a dedicated test directory with a virtual environment.

Follow one of the following two options:

* Set up and use Python virtual environments for Ansible (requires a python version >=3.10)
* Install Miniconda

#### Set up and use Python virtual environments for Ansible

1) First, verify the installed Python version and path

```bash
$ python3 -V
```

Check Python version

```bash
Python 3.13.2
```

If python version <3.10, skip this section and move to section 'Install Miniconda'. 

2) Create a directory for the virtual environment

```bash
mkdir python-venv
cd !$
```

3) Set up Python virtual environments for Ansible

```bash
pip3 install virtualenv
python3 -m venv dbaas 
source dbaas/bin/activate
python3 -m pip install --upgrade pip
```

NOTE: See 'How to set up and use Python virtual environments for Ansible' for further information https://www.redhat.com/en/blog/python-venv-ansible

#### Installing Miniconda:

1) Run the following four commands to download and install the latest Linux installer for your chosen chip architecture. 

Line by line, these commands:

* create a new directory named “miniconda3” in your home directory.
* download the Linux Miniconda installation script for your chosen chip architecture and save the script as miniconda.sh in the miniconda3 directory.
* run the miniconda.sh installation script in silent mode using bash.
* remove the miniconda.sh installation script file after installation is complete.

```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
```

2) After installing, close and reopen your terminal application or refresh it by running the following command:

```bash
source ~/miniconda3/bin/activate
```

3) Then, initialize conda on all available shells by running the following command:

```bash
conda init --all
```

NOTE: See 'Installing Miniconda' for further information https://www.anaconda.com/docs/getting-started/miniconda/install#linux-terminal-installer

#### Install dbaas-ansible-collection

1) Download and extact the zip file with the software

```bash
unzip dbaas-ansible.zip
```

2) Run dbaas_config.sh

```bash
sh dbaas-ansible-collection/dbaas_config.sh 
```

Validate the output:

```bash
Copying ansible.cfg file
Installing dbaas requirements
Installing the ansible dbaas collection
Listing the ansible dbaas collection

# /scratch/salasino/ansible/collections/ansible_collections
Collection   Version
------------ -------
oracle.dbaas 1.0.0 
```

### Included content

<!--start playbook content-->
Playbooks:
  1) oracle.dbaas.onboarding
  2) oracle.dbaas.database
  3) oracle.dbaas.dataguard
  4) oracle.dbaas.framework
<!--end playbook content-->

<!--start collection content-->
Roles:
  1) oracle_facts 
  2) database 
  3) dataguard
<!--end collection content-->

## DBaaS Deployment

### Onboarding

Set the environment variable DBAAS_ENV to the desired name.

```bash
export DBAAS_ENV=ocidbs
```

Execute the Ansible playbook oracle.dbaas.onboarding and provide the password for Ansible Vault:

```bash
ansible-playbook oracle.dbaas.onboarding -i collections/ansible_collections/oracle/dbaas/inventory/localhost.yml
```

Edit the key file, if required:

```bash
ansible-vault edit inventory/$DBAAS_ENV.key --ask-vault-password 
```

Edit the inventory file, if required:

```bash
vi inventory/$DBAAS_ENV.yml 
```

Test the inventory file configuration:

```bash
ansible -i inventory/$DBAAS_ENV.yml all -m setup -a "filter=architecture"
```

TIP: 

```bash
export VAULT_PASSWORD=<Vault_password>; history -d $(history 1)
ansible-playbook oracle.dbaas.database -i inventory/$DBAAS_ENV.yml -e @inventory/$DBAAS_ENV.ini -e @inventory/$DBAAS_ENV.key --limit $DBAAS_ENV --vault-password-file=./inventory/vault_pass --tags onboarding
```

### DBaaS - Create database

Execute oracle.dbaas.dbaas to create a database:

```bash
ansible-playbook oracle.dbaas.database -i inventory/$DBAAS_ENV.yml -e @inventory/$DBAAS_ENV.key -e "version=19.25" --limit dbservers --vault-password-file=./inventory/vault_pass --tags database_create,prereqs
```

### DBaaS - Create standby database

Execute oracle.dbaas.dataguard_configure to create a standby database:

```bash
ansible-playbook oracle.dbaas.dataguard -i inventory/$DBAAS_ENV.yml -e @inventory/$DBAAS_ENV.key --limit dbservers --vault-password-file=./inventory/vault_pass --tags configure,prereqs 
```

### DBaaS - Delete database

Execute oracle.dbaas.dbaas to delete a standby database:

```bash
ansible-playbook oracle.dbaas.database -i inventory/$DBAAS_ENV.yml -e @inventory/$DBAAS_ENV.key --limit dbservers --vault-password-file=./inventory/vault_pass --tags database_delete,standby
```

Execute oracle.dbaas.dbaas to delete a primary and standby database:

```bash
ansible-playbook oracle.dbaas.database -i inventory/$DBAAS_ENV.yml -e @inventory/$DBAAS_ENV.key --limit dbservers --vault-password-file=./inventory/vault_pass --tags database_delete,primary
```

## DBaaS without Inventory 

```bash
ansible-playbook oracle.dbaas.database -i '<comma_separated_list_of_hosts>' -e "target=all group_names=dbservers database_list=<primary_db_name>" --tags oracle_facts
ansible-playbook oracle.dbaas.database -i '<comma_separated_list_of_hosts>' -e "target=all group_names=dbservers database_list=<primary_db_name> db_unique_name_standby_suffix=stby1" --tags cofigure,prereqs 
```

## Changes

See CHANGELOG__.

__ https://github.com/oracle-samples/maa/blob/main/CHANGELOG.rst

## Contributing

oci-cli is an open source project. See CONTRIBUTING__ for details.

Oracle gratefully acknowledges the contributions to oci-cli that have been made by the community.

__ https://github.com/oracle-samples/maa/blob/main/CONTRIBUTING.md

## Roadmap

<!-- Optional. Include the roadmap for this collection, and the proposed release/versioning strategy so users can anticipate the upgrade/update cycle. -->

## Known Issues

- [oracle-samples/maa/issues](https://github.com/oracle-samples/maa/issues)
- [High Availability Overview and Best Practices - Troubleshooting Oracle GoldenGate](https://docs.oracle.com/en/database/oracle/oracle-database/19/haovw/ogg-troubleshooting1.html)

## Licensing

Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.

This SDK and sample is dual licensed under the Universal Permissive License 1.0 and the Apache License 2.0.

See LICENSE__ for more details.

__ https://github.com/oracle-samples/maa/blob/main/LICENSE.txt
