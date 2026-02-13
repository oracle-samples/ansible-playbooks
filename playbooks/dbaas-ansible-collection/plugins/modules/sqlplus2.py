#!/usr/bin/python

#
# Oracle Database as a Service 
#
# Copyright (c) 2022 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at
# https://oss.oracle.com/licenses/upl.
#
# Description: Playbook to perform various life-cycle and administration operations on Oracle Exadata Database Service, BaseDB and on-prem. 
#
# DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS HEADER.

from __future__ import (absolute_import, division, print_function)
from subprocess import Popen, PIPE
from os.path import abspath, dirname, join
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_test

short_description: This is my test module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str
    new:
        description:
            - Control to demo if the result of this module is changed or not.
            - Parameter description can be a list as well.
        required: false
        type: bool
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
# extends_documentation_fragment:
#     - my_namespace.my_collection.my_doc_fragment_name

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''

import subprocess
import os
from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        oracle_home=dict(type='str', required=True),
        oracle_sid=dict(type='str', required=True),
        query=dict(type='str', required=True),
        new=dict(type='bool', required=False, default=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        oracle_home='',
        oracle_env='',
        query='',
        results=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['oracle_home'] = module.params['oracle_home']
    result['oracle_sid'] = module.params['oracle_sid']
    result['query'] = module.params['query']
    result['results'] = (run_sqlplus(module.params['oracle_home'],module.params['oracle_sid'],module.params['query']))[1:-1]

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['new']:
        results['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['query'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def run_sqlplus(oracle_home,oracle_sid,query):

    # Run a sql command or group of commands against
    # a database using sqlplus.

    sqlplus = os.path.join(oracle_home, 'bin/sqlplus')
    sql_query = "set feedback off" + "\n" + "SET MARKUP CSV ON QUOTE OFF" + "\n" + query
    # my_env = {**os.environ, **oracle_sid}
    my_env = {'ORACLE_HOME': oracle_home, 'ORACLE_SID': oracle_sid, **os.environ}
    
    p = subprocess.Popen(
                            [sqlplus,'-L','-F','-SILENT','/ as sysdba'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            env=my_env
                        )
    (stdout,stderr) = p.communicate(sql_query.encode('utf-8'))
    stdout_lines = stdout.decode('utf-8').split("\n")

    return stdout_lines

def main():
    run_module()

if __name__ == '__main__':
    main()