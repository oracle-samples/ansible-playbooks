#!/bin/bash
if [ ! -d "python-venv" ]; then
  echo "Installing Python module virtualenv"
  pip3 install virtualenv > /dev/null 2>&1
  echo "Creating python virtual env"
  python3 -m venv dbaas 
  echo "Activating python virtual env"
  source dbaas/bin/activate
  echo "Upgrading python pip"
  python3 -m pip install --upgrade pip
else
  echo "Activating python virtual env"
  source dbaas/bin/activate
fi
