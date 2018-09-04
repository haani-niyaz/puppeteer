# puppeteer

*An opinionated way to manage your Ansible projects.*

<img src="images/puppeteer.png" width="150" height="150">

<sub> A portion of this image was sourced from <a href="https://www.freepik.com/free-photos-vectors/business">Author Dooder - Freepik.com</a></sub>


## Motivation

TBA.

## Installation

`pip install --user git+https://github.com/haani-niyaz/puppeteer.git`


## Quick Start


### Setup

Add a `.puppeteer.yml` file to your ansible control repo. An example is provided below:

```
 # Mandatory to provide environments
control_repo:
  # List of environments in 'environments' directory.
  # if sub directories exist, seperate them with '/' i.e: 'aws/dev'
  environments:
   - dev
   - test
   - staging
   - prod
  # Override inventory file name if required. default is 'inventory.ini'
  inventory_file_name: 'inventory'

# Optionally add config to your ansible.cfg file
ansible_config:
  defaults:
    host_key_checking: False
    callback_whitelist: 'profile_tasks'
    roles_path: 'roles'
  ssh_connection:
    pipelining: True
    control_path: '/tmp/ansible-ssh-%%h-%%p-%%r'
```

### Available Commands

```
$ puppeteer --help

usage: puppeteer [-h] [-v] [sub-command] ...

Utility to manage Ansible workflow

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit

sub commands:
  [sub-command]  -h, --help
    tag-role     tag a role in repo file
    list-roles   list roles in repo file
    fetch-roles  fetch roles
    init         generate layout for a new project or reinitialize an existing
                 project
    set-config   generate ansible.cfg file
    show-config  show ansible.cfg file
    deploy       all in one action to fetch roles and generate ansible.cfg
                 file 
```
