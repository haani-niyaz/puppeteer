# puppeteer

*An opinionated way to manage your Ansible projects.*

<img src="images/puppeteer.png" width="200" height="150">

<sub> A portion of this image was sourced from <a href="https://www.freepik.com/free-photos-vectors/business">Author Dooder - Freepik.com</a></sub>

## Installation

`pip install --user git+https://github.com/haani-niyaz/puppeteer.git`


## Motivation

Git is a powerful tool but managing environments as 'branches' in my experience can quickly become non trivial. A better way is the [Github git flow](https://guides.github.com/introduction/flow/). Combined with the alternative style of setting up your [repository structure](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html#alternative-directory-layout) provides a straight forward and simple workflow to manage your Ansible projects.


### Benefits

- Less time spent fighting configuration drift between branches.
- Follow a human friendly process instead of relying on git command flows e.g: `git cherry-pick` to bring across specific changes from one branch to another.
- Master branch is protected from inheriting broken changes; Anything in the `master` branch is deployable.
- Rolling back is quick and easy; zero code touch since we deploy from our stable `master` branch.
- Etc.

### Where does `puppeteer` fit in?

`puppeteer` is designed to enable the methodology described above and provides shortcuts to easily conform to this workflow.

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
    dev-role     develop and test role locally against a target environment
    list-roles   list all roles requirements.yml file
    fetch-roles  fetch roles
    init         generate layout for a new project or reinitialize an existing
                 project
    set-config   generate ansible.cfg file
    show-config  show ansible.cfg file
    deploy       all in one action to fetch roles and generate ansible.cfg
                 file
```

## Puppeteer in Action

### Create Project

To begin using `puppeteer` a `.puppeteer.yml` file must exist in your project's root directory.  This file contains a list of mandatory environments to initialize the `puppeteer` cli. Ansible settings should also be added to this file if required.

Let's begin by creating the `.puppeteer.yml` file with 3 environments and an optional Ansible parameter:


```
$ mkdir project
$ cat >> .puppeteer.yml << EOF
control_repo:
  environments:
   - dev
   - test
   - prod   
ansible_config:
  defaults:
    host_key_checking: False
EOF

```

<sub>**ansible.cfg**</sub> 

<sub>`puppeteer` dynamically generates the `ansible.cfg` file and most notably updates the inventory path. This allows you to run `ansible-playbook sample.yml` instead of `ansible-playbook -i environments/dev/inventory.ini sample.yml` since the target environment is already updated in `ansible.cfg` file.</sub>


Now you can proceed to initialize your project:

```
$ puppeteer init
+ Initializing environments..
✓ Done.
```

The `init` sub-command will generate an `environments` directory with the following structure:

```
environments
├── dev
│   ├── group_vars
│   ├── host_vars
│   ├── inventory.ini
│   ├── requirements.yml
│   └── roles
├── prod
│   ├── group_vars
│   ├── host_vars
│   ├── inventory.ini
│   ├── requirements.yml
│   └── roles
└── test
    ├── group_vars
    ├── host_vars
    ├── inventory.ini
    ├── requirements.yml
    └── roles
```

This structure tightly aligns with the alternative style of setting up your Ansible [repository structure](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html#alternative-directory-layout).


### Fetching Roles and Targetting an Environment

Fetch all the roles from the target environment's `requirements.yml` file and updates
the `ansible.cfg` with the pre-defined configuration:

```
$ puppeteer deploy dev
+ Fetching roles...
- extracting plone.plone_server to /private/tmp/environments/dev/roles/plone.plone_server
- plone.plone_server (1.3.6) was installed successfully
- extracting jnv.unattended-upgrades to /private/tmp/environments/dev/roles/jnv.unattended-upgrades
- jnv.unattended-upgrades (v1.5.0) was installed successfully
 ✓ Done.
You are now working on 'dev'
```

This all-in-one command will download all roles to the target environment's `roles` directory and update the inventory file path to match the target environment. If the roles already exist you can provide the `--force` option to overwrite.

This simple command allows you to easily switch between environments with the latest code base.

### Check Generated Config

The built-in command to display the generated `ansible.cfg` file:

```
$ puppeteer show-config
[defaults]
inventory = environments/dev/inventory.ini
host_key_checking = False
```

### Target a Different Environment

Change the inventory path but ignore downloading roles:

```
$ puppeteer set-config test
You are now working on 'test'
```

### Fetch Roles

Download roles for a specific environment but ignore changing inventory path:

```
$ puppeteer fetch-roles dev
fetch-roles -f dev
+ Fetching roles...
- changing role plone.plone_server from 1.3.6 to 1.3.6
- extracting plone.plone_server to /private/tmp/environments/dev/roles/plone.plone_server
- plone.plone_server (1.3.6) was installed successfully
- changing role jnv.unattended-upgrades from v1.5.0 to v1.5.0
- extracting jnv.unattended-upgrades to /private/tmp/environments/dev/roles/jnv.unattended-upgrades
- jnv.unattended-upgrades (v1.5.0) was installed successfully
 ✓ Done.
```


### View Roles

Display an environment's `requirements.yml` file:

```
$ puppeteer list-roles dev
---

- src: https://github.com/plone/ansible.plone_server.git
  version: 1.3.6
  name: plone.plone_server

- src: https://github.com/jnv/ansible-role-unattended-upgrades.git
  version: v1.5.0
  name: jnv.unattended-upgrades
```

### Tag a Role

Tag a role the target environment's `requirements.yml` file:

```
# tag role 'foo' to version '2.0.0' in dev requirements.yml file
$ puppeteer tag-role foo -t 2.0.0 -e dev
```

You also have the option to tag all environments:

```
# tag role 'foo' to version '2.0.0' in dev,test,prod requirements.yml file
$ puppeteer tag-role foo -t 2.0.0 -e all
```

<sub>**Tip:** run `puppeteer tag-role --help` to get examples and more information.</sub>


### Local Role Development

It is considered best practice to develop and validate (see [molecule](https://molecule.readthedocs.io/en/stable/)) roles in isolation with sane defaults. However, there are instances when a role may need to be tested on a specific environment due to dependencies that cannot be satisfied locally. The results of this testing may also contribute to application logic fixes or changes. So if you are looking to test a role on a target environment prior to making any code commits you can leverage this option.

Let's take a look at what `puppeteer` provides to enable this process.

#### Setup

 Assuming you have a role named `foo`, clone repo `foo` to `~/.puppeteer/roles` (or run `ansible-galaxy init ~/.puppeteer/roles` for a new role). You can use your own workspace location if you wish but `puppeteer` by default looks for the role in the base directory `~/.puppeteer/roles`.

#### Link Development Role to Target Environment

If you wish to target an environment but use the role in development `~/.puppeteer/roles/foo` you can simply run:

`$ puppeteer dev-role foo -e dev`

The command symlinks from `environments/dev/roles/foo` to the default workspace `~/.puppeteer/roles/foo`.This allows you to make changes in `~/.puppeteer/roles/foo` whilst testing your codebase in the dev environment.

<sub>**Tip:** run `puppeteer dev-role --help` to get examples and more information.</sub>

#### Cleanup

If you wish to unlink the role from the environment to the workspace use the `--clean` option.

`$ puppeteer dev-role -e dev --clean`





