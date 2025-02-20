# Oracle Linux Automation Manager 2.2 Cluster

The playbook provides a clustered installation of [Oracle Linux Automation Manager](https://docs.oracle.com/en/operating-systems/oracle-linux-automation-manager/) using the details from an inventory file.

It configures the following seven nodes:

- A remote database
- Two control plane nodes
- Two local execution nodes
- A hop node and a remote execution node

## Quickstart

### Assumptions

1. You have all the hosts running
1. You have setup the required OpenSSH keys
1. You have the necessary permissions and access

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
    cd ol-playbooks/playbooks/OLAM/cluster-plus-hop-node
    cp group_vars/all.yml.example group_vars/all.yml
    cp inventory/hosts.ini.example inventory/hosts.ini
    ```

1. Edit the group variables, change the default passwords and replace the sample ssh key files:

    ```
    # Create Linux non-opc user account for installing Oracle Linux Automation Manager
    
    "username": oracle
    
    # Enter the non-hashed password for the non-opc user account.
    
    "user_default_password": oracle

    # Enter the password for postgress awx user

    "awx_pguser_password": CHANGE_ME

    # Enter the password for PostgreSQL awx user

    "olam_admin_password": CHANGE_ME

    # Enter the name of a local ssh keypair pub file located in the ~/.ssh directory. This key appends
    # to the non-opc user account's authorized_keys file. Replace <username> and <keypair> with
    # your user.

    "ssh_keyfile": /home/<username>/.ssh/<keypair>.pub
    ```

    This file also contains a variable for setting a proxy if required to reach the internet from the Oracle Linux Automation Manager nodes.

1. Edit the inventory and customize hostnames:

    ```
    [control_nodes]
    olam-control01
    olam-control02

    [control_nodes:vars]
    node_type=control
    peers=local_execution_group

    [execution_nodes]
    olam-execution01
    olam-execution02
    olam-remote-execution01
    olam-hop01

    [local_execution_group]
    olam-execution01
    olam-execution02

    [local_execution_group:vars]
    node_type=execution

    [hop]
    olam-hop01

    [hop:vars]
    peers=control_nodes

    [remote_execution_group]
    olam-remote-execution01

    [remote_execution_group:vars]
    peers=hop

    [db_nodes]
    olam-db

    [all:vars]
    ansible_user=opc
    ansible_ssh_private_key_file=~/.ssh/oci-olam
    ansible_python_interpreter=/usr/bin/python3
    ```    
    
    The `all:vars` group variables define the user, key file, and python version used when connecting to the different nodes using SSH.

    A second `host.ini.example` is provided in the inventory directory for a four node cluster without hop-node and remote exexution node.

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

    ansible-playbook -i inventory/hosts.ini install.yml
    ```

## Resources

[Oracle Linux Automation Manager Training](https://www.oracle.com/goto/linuxautomationlearning)    
[Oracle Linux Training Station](https://www.oracle.com/goto/oltrain)     






