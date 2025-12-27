Role Name
=========

A brief description of the role goes here.

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

Role Variables
--------------

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

dbhome_create:
ansible-playbook oracle.dbaas.dbaas --limit <env_name> -e @inventory/envs/<env_name>.ini -e "targetVersion=23412406" --tags dbhome_create
ansible-playbook oracle.dbaas.dbaas --limit <env_name> -e @inventory/envs/<env_name>.ini -e "targetVersion=23.5.0.24.07" --tags dbhome_create
ansible-playbook oracle.dbaas.dbaas --limit <env_name> -e @inventory/envs/<env_name>.ini -e "targetHome=/u01/app/oracle/product/23.6.0.24/db_home_2306241127 goldImage=/ade_autofs/ud222_db/RDBMS_23.0.0.0.0_LINUX.X64.rdd/241127/install/shiphome/goldimage/db_home.zip" --tags dbhome_create

database_create:
ansible-playbook oracle.dbaas.dbaas --limit <env_name> -e @inventory/envs/<env_name>.ini -e "targetVersion=23.5.0.24.07" --tags database_create
ansible-playbook oracle.dbaas.dbaas --limit <env_name> -e @inventory/envs/<env_name>.ini -e "targetHome=/u01/app/oracle/product/23.5.0.24/db_home_23502407" --tags database_create

swingbench_configure:
ansible-playbook oracle.dbaas.onboarding --limit slc1 -e @inventory/envs/slc1.ini --tags swingbench_configure

create_standby_database:
ansible-playbook oracle.dbaas.onboarding --limit slc1 -e @inventory/envs/slc1.ini --tags create_standby_database --extra-vars "targetVersion=23502407"

DBaaSCLI command:
ansible-playbook oracle.dbaas.dbaas --limit hdg --extra-vars @inventory/envs/hdg1.ini --extra-vars "dbaascli_command='database modifyParameters --setParameters db_writer_processes=32,log_archive_trace=551 --allowBounce' log_analyze_flag=true" --tags dbaascli
ansible-playbook oracle.dbaas.dbaas -i inventory/oci.ini --limit hdg --extra-vars @inventory/envs/hdg1.ini --extra-vars "dbaascli_command='database move' oracleHomeName='OraHome3'" --tags dbaascli 

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
