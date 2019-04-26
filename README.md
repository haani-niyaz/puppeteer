# puppeteer

*An opinionated way to manage your Ansible projects.*

<img src="images/puppeteer.png" width="200" height="150">

<sub> A portion of this image was sourced from <a href="https://www.freepik.com/free-photos-vectors/business">Author Dooder - Freepik.com</a></sub>

## Installation

`pip install --user git+https://github.com/haani-niyaz/puppeteer.git`


## Motivation

Git is a powerful tool but managing environments as 'branches' in my experience can quickly become non trivial. A better way is the [Github git flow](https://guides.github.com/introduction/flow/). Combined with the alternative style of setting up your [repository structure](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html#alternative-directory-layout) proivdes a straight forward and simple workflow to manage your Ansible projects.


### Benefits

- Less time spent fighting configuration drift between branches
- Follow a human friendly process instead of relying on git command flows e.g: `git cherry-pick` to bring across specific changes from one branch to another.
- Master branch is protected from inheriting broken changes; Anything in the `master` branch is deployable.
- Rolling back is quick and easy; zero code touch since we deploy from our stable `master` branch.
- Etc.

### Where does `puppeteer` fit in?

`puppeteer` is designed to conform to the above methodology and provides the shortcuts to enable this workflow.

## Quick Start


### Setup

Add a `.puppeteer.yml` file to your ansible repo. An example is provided below:

```
# Mandatory to provide environments
control_repo:
  # List of environments in 'environments' directory.
  # If sub directories exist, seperate them with '/' i.e: 'aws/dev'
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
    tag-role     update version in requirements.yml file
    list-roles   list all roles requirements.yml file
    fetch-roles  fetch roles
    init         generate layout for a new project or reinitialize an existing
                 project
    set-config   generate ansible.cfg file
    show-config  show ansible.cfg file
    deploy       all in one action to fetch roles and generate ansible.cfg
                 file
```