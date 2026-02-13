#!/bin/bash
if [ ! -d "collections/ansible_collections/oracle/dbaas" ]; then
  echo "Copying ansible.cfg file"
  cp dbaas-ansible-collection/ansible.cfg .
  echo "Installing dbaas requirements"
  python3 -m pip install -r dbaas-ansible-collection/requirements.txt > /dev/null 2>&1
  echo "Installing the ansible dbaas collection"
  ansible-galaxy collection install dbaas-ansible-collection -p ./collections > /dev/null 2>&1
  echo "Listing the ansible dbaas collection"
  ansible-galaxy collection list oracle.dbaas
else
  echo "Upgrading the ansible dbaas collection"
  ansible-galaxy collection install dbaas-ansible-collection -p ./collections --upgrade
  echo "Listing the ansible dbaas collection"
  ansible-galaxy collection list oracle.dbaas
fi
