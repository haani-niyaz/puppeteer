"""Application behaviour"""

import sys
from time import sleep
import cmdopts
from .colourize import color
from .fileops import FileOps, YAMLFile, YAMLFileError
from .actions.controlrepo import ControlRepo, ControlRepoError
from .actions.inigen import AnsibleConfig
from .actions.role import Role, RoleError
from .constants import USER_CONFIG_FILE, ANSIBLE_CONFIG_FILE, PROJECT_URL, CROSS, TICK


def execute_tag_role(name, tag, env):
  """Control flow to tag a role

  Args:
      name (str): role name
      tag (str): new version
      env (str): target environment
  """
  try:
    role = Role(env)
    print(color('cyan', '+ Updating {0} environment..'.format(env)))
    updated_repo_data = role.tag(name, tag)
    role.update_repo_file(updated_repo_data)
    print(color('green', role.get_tag(name)))
    print(color('cyan', "{0} Done.".format(TICK)))
  except RoleError, e:
    if e.ec == RoleError.EXISTS:
      print(color('yellow', e.message + ' in {0}'.format(env)))
    else:
      print(color('red', "{0} {1}".format(CROSS, e.message)))
      sys.exit(1)


def execute_fetch_roles(env, force):
  """Control flow to fetch roles

Args:
  env (str): target environment
  force (str): option to force download
"""
  roles = Role(env)
  print(color('cyan', '+ Fetching roles...'))
  try:
    roles.fetch('--force') if force else roles.fetch()
    print(color('cyan', "{0} Done.".format(TICK)))
  except RoleError, e:
    # Omit space because output starts with a blank space
    print(color('red', "{0}{1}".format(CROSS, e.message)))
    sys.exit(1)


def main():

  # Parser relies on dynamically loading environments from the user cofig
  # so let's attempt to get the list of environments first

  try:
    # Read config provided by user in '.puppeteer.yml'
    user_config = YAMLFile(USER_CONFIG_FILE)
    user_config_data = user_config.read()

    try:
      # Only initialize control repo object if the user config defines 'control_repo' var
      if 'control_repo' in user_config_data:
        # Validate environments list when initializing control repo object
        control_repo = ControlRepo(user_config_data['control_repo'])
      else:
        err_msg = ".puppeteer.yml is missing control repo var. Please see setup details at {0}.".format(
            PROJECT_URL)
        print(color('red', "{0} {1}".format(
            CROSS, err_msg)))
        sys.exit(1)
    except ControlRepoError as e:
      print(color('red', "{0} {1}".format(CROSS, e)))
      sys.exit(1)

  except YAMLFileError, e:
    print(color('red', "{0} {1}".format(CROSS, e)))
    sys.exit(1)

  # Now we can initialize the parser with the environments list
  parser = cmdopts.main(control_repo.envs)
  cli = parser.parse_args()

  ### Operations ###

  # Initialize repository
  if cli.sub_cmd == 'init':

    try:
      print(color('cyan', '+ Initializing environments..'))
      control_repo.create_layout()
      sleep(0.4)
      print(color('cyan', "{0} Done.".format(TICK)))

    except ControlRepoError, e:
      print(color('red', e))
      sys.exit(1)

  # Show ansible.cfg
  elif cli.sub_cmd == 'show-config':

    try:
      ansible_config_file = FileOps(ANSIBLE_CONFIG_FILE)
      print(ansible_config_file.show())
    except YAMLFileError as e:
      print(color('red', "{}. Have you run 'puppeteer set-config' yet?".format(e)))

  # Setup user config in ansible.cfg
  elif cli.sub_cmd == 'set-config':

    ansible_cfg = AnsibleConfig(
        user_config_data['ansible_config'], inventory_file=control_repo.inventory_file, env=cli.env)
    ansible_cfg.create()
    print(color('cyan', "You are now working on '{0}'".format(cli.env)))

  # List all roles
  elif cli.sub_cmd == 'list-roles':

    try:
      role = Role(cli.env)
      print(role.list_roles())
    except RoleError as e:
      print(color('red', "{0} {1}".format(CROSS, e.message)))
      sys.exit(1)

  # Get all roles
  elif cli.sub_cmd == 'fetch-roles':

    execute_fetch_roles(cli.env, cli.force)

  # Tag a role
  elif cli.sub_cmd == 'tag-role':

    if cli.env == 'all':
      for env in control_repo.envs:
        execute_tag_role(cli.name, cli.tag, env)
    else:
      execute_tag_role(cli.name, cli.tag, cli.env)

  # Get all roles and setup user config in ansible.cfg file
  elif cli.sub_cmd == 'deploy':

    execute_fetch_roles(cli.env, cli.force)

    ansible_cfg = AnsibleConfig(
        user_config_data['ansible_config'], inventory_file=control_repo.inventory_file, env=cli.env)
    ansible_cfg.create()
    print(color('cyan', "You are now working on '{0}'".format(cli.env)))

  elif cli.sub_cmd == 'dev-role':

    try:
      role = Role(cli.env)
    except RoleError as e:
      print(color('red', "{0} {1}".format(CROSS, e.message)))
      sys.exit(1)

    if cli.clean:
      try:
        role.unsymlink_local_role(cli.name)
        print(
            color('cyan', "{0} Remove symlink 'environments/{1}/roles/{2}' to workspace '{3}'".
                  format(TICK, cli.env, cli.name, role.workspace)))
      except RoleError as e:
        if e.ec == RoleError.EXISTS:
          print(color('yellow', e.message))
          sys.exit(0)
        print(color('red', "{0} {1}".format(CROSS, e.message)))
        sys.exit(1)
    else:
      try:
        role.symlink_local_role(cli.name, cli.workspace)
        print(
            color('cyan', "{0} Created symlink 'environments/{1}/roles/{2}' to workspace '{3}'".
                  format(TICK, cli.env, cli.name, role.workspace)))
      except RoleError as e:
        print(color('red', "{0} {1}".format(CROSS, e.message)))
        sys.exit(1)

  else:
    parser.print_help()
