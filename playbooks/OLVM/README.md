# OLVM - Ansible Playbooks for Oracle Linux Virtualization 


A collection of Ansible playbooks to use with Oracle Linux Virtualization Manager. Playbooks are tested with Ansible CLI commands on Oracle Linux and with Oracle Linux Automation Manager.

The playbooks uses modules from the [`ovirt.ovirt` Ansible collection](https://docs.ansible.com/ansible/latest/collections/ovirt/ovirt/index.html) which should be downloaded before using the playbooks. Read the collection documentation page for additional explanation or for extending the functionality of the playbooks.

## How to use the playbooks

### Ansible CLI

First step is the configuration of the playbook variables which are mostly configured in ``default_vars.yml`` file. Variables may be used in the command line when not configured in the default variables file. Variables are required to configure your infrastructure settings for the OLVM server, VM configuration and cloud-init. See below table for explanation of the variables. 

For example, the playbooks can be used like this (adjust variables to your infrastructure):

    $ git clone https://github.com/oracle-samples/ansible-playbooks.git ol-playbooks
    $ cd ol-playbooks/playbooks/OLVM
    $ ansible-galaxy collection install -f ovirt.ovirt
    $ ansible-galaxy collection install -f community.general
    $ vi default_vars.yml
    $ export "OVIRT_URL=https://olvm-engine.demo.local/ovirt-engine/api"
    $ export "OVIRT_USERNAME=admin@internal"
    $ export "OVIRT_PASSWORD=CHANGE_ME"

    # create a single VM
    $ ansible-playbook -i olvm-engine.demo.local, -u opc --key-file ~/.ssh/id_rsa \
        -e "vm_name=vm01" -e "vm_ip_address=192.168.1.101" \
        olvm_create_one_vm.yml

    # create multiple VMs with inventory file, see example hosts.ini file
    $ ansible-playbook -i inventory/hosts.ini -u opc --key-file ~/.ssh/id_rsa \
        olvm_create_multiple_vms.yml

    # delete a VM
    $ ansible-playbook -i olvm-engine.demo.local, -u opc --key-file ~/.ssh/id_rsa \
        -e "vm_name=vm01" olvm_delete_vm.yml

    # live migrate a VM
    $ ansible-playbook -i olvm-engine.demo.local, -u opc --key-file ~/.ssh/id_rsa \
        -e "vm_name=vm01" -e "dst_kvmhost=KVM2" olvm_migrate_vm.yml

Note 1: using the OLVM server FQDN (in this example olvm-engine.demo.local), appended with a comma, is a quick-way to not use a inventory file.

Note 2: as it includes clear-text password, for better security you may want to encrypt the ``default_vars.yml`` file with the `ansible-vault` command. When running the playbook, Ansible asks for a secret to decrypt the YAML file.

    $ ansible-vault encrypt default_vars.yml
    $ ansible-playbook -i olvm-engine.demo.local, -u opc --key-file ~/.ssh/id_rsa \
        -e "vm_name=oltest" -e "vm_ip_address=192.168.1.100" \
        --ask-vault-pass olvm_create_single_vm.yml

### Oracle Linux Automation Manager

#### Project:
In Oracle Linux Automation Manager you can directly import the playbook repository from GitHub as project. The top-level directory of the repository contains the requirements file to download the `ovirt.ovirt` ansible collection.

#### Inventory:
Create an inventory and add one host with the details of your OLVM server, this is the target host were you run the playbook. Make sure you have a Machine credential setup for this host so that ansible can SSH to it (run the ping Module for this host). For the VMs you want to create add an  inventory group ``[instances]`` and add the VM names including hostvars for ``vm_name`` and ``vm_ip_address``.

#### Credentials:
Besides the standard SSH credential to access the target host, an additional credential is required to use the ovirt modules in the playbooks. It's based on credential type ``Red Hat Virtualization`` and you need to fill in the OLVM FQDN, username, password and CA File. For example:

    Host (Authentication URL): 	https://olvm-engine.demo.local/ovirt-engine/api
    Username:			admin@internal
    Password:			CHANGE_ME

#### Templates:
Create a new job template and provide the following information:

    Inventory:		Select the inventory containing the OLVM host
    Project:		Select project from the Github repository
    Playbook:		Select playbook from Project, for example olvm_create_single_vm.yml
    Credentials:		Select Machine (SSH) credential and the Virtualization credentials
    Variables:		Enter the variables as used in the example default_vars.yml file

### Secure API connection

By default the API connection to the OLVM server is insecure, if you want to use a secure API connection then you need to define variable ``olvm_insecure`` and make sure the CA file is available (default location is ``/etc/pki/ovirt-engine/ca.pem``). You may use ``olvm_cafile`` to specify alternative location. 

    olvm_insecure: false
    olvm_cafile: /home/opc/ca.pem

The CA file can be downloaded from the main OLVM web portal or directly from the OLVM server, for example:

    $ scp root@olvm-engine.demo.local:/etc/pki/ovirt-engine/ca.pem /home/opc/ca.pem

## Variables used in the playbooks 

| Variable | Example value | Description |
| -------- | ------------- | ----------- |
| OVIRT_URL | https://olvm-fqdn/ovirt-engine/api | The API URL of the OLVM server
| OVIRT_USERNAME | admin@internal | The name of the user, same as used for GUI login
| OVIRT_PASSWORD | CHANGE_ME | The password of the user, same as used for GUI login
| olvm_cluster | Default | Name of the cluster, where VM should be created
| olvm_template | OL9U4_x86_64-olvm-b234 |Name of the template, which should be used to create VM
| vm_name | oltest | Name of the VM, will also be used as hostname
| vm_ip_address | 192.168.1.100 | Static IP address of VM, if DHCP is required cloud-init section in playbook should be changed
| vm_ram | 2048MiB | Amount of memory of the VM
| vm_cpu | 4 | Number of virtual CPUs sockets of the VM
| vm_root_passwd | your_secret_root_pw | Root password of the VM, used bu cloud-init
| vm_dns | 192.168.1.3 | DNS server to be used for VM
| vm_dns_domain | demo.local | DNS domainto to be used for VM
| vm_gateway | 192.168.1.1 | Default gateway to be used for VM
| vm_netmask | 255.255.255.0 | Netmask to be used for VM
| vm_timezone | Europe/Amsterdam | Timezone for VM
| vm_user | opc | Standard user for Oracle provided template, otherwise use your own or root user
| vm_user_sshpubkey | "ssh-rsa AAAA...YOUR KEY HERE...hj8= " | SSH Public key for stndard user
| src_vm | oltest | VM used as source VM for cloning operation
| src_vm_snapshot | base_snapshot | Name of snapshot of source VM, for cloning operation 
| dst_vm | oltest_cloned | Name of destination VM for cloning operation
| dst_kvmhost | KVM2 | Name (not hostname) of kvm host in OLVM cluster and destination for live-migration
| vm_id | 76c76c8b-a9ad-414e-8274-181a1ba8948b | VM ID for the VM, used for rename of VM
| vm_newname | oltest | New name for VM with vm_id, used for rename of VM
| olvm_insecure | false | By default ``true``, but define ``false`` in case you need secure API connection
| olvm_cafile | /home/opc/ca.pem | Location of CA file in case you wish alternative location


## Deploying Oracle Linux OLVM VM templates

Two playbooks are provided to deploy new virtual machines in Oracle Linux Virtualization Manager based on a pre-configured template. This may be your own template or templates downloaded from Oracle's website which can be [imported directly in Oracle Linux Virtualization Manager](https://docs.oracle.com/en/virtualization/oracle-linux-virtualization-manager/admin/admin-admin-tasks.html#templates-create):

* [Free Oracle Linux templates](https://yum.oracle.com/oracle-linux-templates.html)
* [Single Instance and Oracle Real Application Clusters (RAC) templates](https://www.oracle.com/database/technologies/rac/vm-db-templates.html)

The Oracle provided templates use cloud-init to automate the initial setup of virtual machines and cloud-init variables are included in the playbooks.

