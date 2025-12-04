# Oracle Linux Automation Manager 2.2 Single Host Deployment

The playbook provides a single host installation of [Oracle Linux Automation Manager](https://docs.oracle.com/en/operating-systems/oracle-linux-automation-manager/) using the details from an inventory file.

It configures a single node with the following roles:

- database
- control plane
- execution

Playbooks are copied from earlier work in [linux-virt-labs Github repository](https://github.com/oracle-devrel/linux-virt-labs) and adjusted for a generic installation..

## Quickstart

### Assumptions

1. You have one Oracle Linux 8 host running
1. You have setup the required OpenSSH keys
1. You have the necessary permissions and access for the target host user with sudo access

### Pre-requisites

1. Git is installed
1. SSH client is installed and configured
1. The `ansible` or `ansible-core` package is installed

### Instructions
---

#### Provisioning using this git repo

1. Clone the repo:

    ```
    git clone https://github.com/oracle-samples/ansible-playbooks.git ol-playbooks
    cd ol-playbooks/playbooks/OLAM/single-node
    cp group_vars/all.yml.example group_vars/all.yml
    cp inventory/hosts.ini.example inventory/hosts.ini
    ```

1. Edit the group variables:

    ```
    # Enter the password for postgress awx user

    "awx_pguser_password": CHANGEME

    # Enter the password for OLAM admin user

    "olam_admin_password": CHANGEME

    # NOTE: use these passwords for demo purposes only, use other ansible features to
    # protect your passwords such as using ansible-vault to encrypt passwords.
    ```

    This file also contains a variable for setting a proxy if required to reach the internet from the Oracle Linux Automation Manager nodes.

1. Edit the inventory:

    ```
    [control]
    my_olam_node
    
    [all:vars]
    ansible_user=opc
    ansible_ssh_private_key_file=~/.ssh/id_rsa
    ansible_python_interpreter=/usr/bin/python3
    ```    
    
    The `all:vars` group variables define the user, key file, and python version used when connecting to the different nodes using SSH.

1. Test SSH connectivity to all the hosts listed in the inventory:

    ```
    ansible-playbook -i inventory/hosts.ini pingtest.yml
    ```

1. Install collection dependencies:

    ```
    ansible-galaxy install -r requirements.yml
    ```
    
1. Run the playbook:

    ```

    ansible-playbook -i inventory/hosts.ini deploy_olam_single.yml
    ```

## Resources

[Oracle Linux Automation Manager Training](https://www.oracle.com/goto/linuxautomationlearning)    
[Oracle Linux Training Station](https://www.oracle.com/goto/oltrain)     






