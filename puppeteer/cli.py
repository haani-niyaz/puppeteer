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

    ansible_config_file = FileOps(ANSIBLE_CONFIG_FILE)
    print(ansible_config_file.show())

  # Setup user config in ansible.cfg
  elif cli.sub_cmd == 'set-config':

    ansible_cfg = AnsibleConfig(
        user_config_data['ansible_config'], inventory_file=control_repo.inventory_file, env=cli.env)
    ansible_cfg.create()
    print(color('cyan', "You are now working on '{0}'".format(cli.env)))

  # List all roles
  elif cli.sub_cmd == 'list-roles':

    role = Role(cli.env)
    print(role.list_roles())

    # Get all roles
  elif cli.sub_cmd == 'fetch-roles':

    roles = Role(cli.env)
    print(color('cyan', '+ Fetching roles...'))
    try:
      roles.fetch('--force') if cli.force else roles.fetch()
      print(color('cyan', " {0} Done.".format(TICK)))
    except RoleError, e:
      print(color('red', "{0} {1}".format(CROSS, e.message)))
      sys.exit(1)

    # Tag a role
  elif cli.sub_cmd == 'tag-role':

    try:
      role = Role(cli.env)
      updated_repo_data = role.tag(cli.name, cli.tag)
    except RoleError, e:
      if e.ec == RoleError.EXISTS:
        print(color('yellow', e.message))
        sys.exit(0)
      else:
        print(color('red', "{0} {1}".format(CROSS, e.message)))
        sys.exit(1)

    try:
      role.update_repo_file(updated_repo_data)
      print(color('cyan', '+ Updating..'))
      print(color('green', role.confirm_tag(cli.name)))
      sleep(0.4)
      print(color('cyan', " {0} Done.".format(TICK)))
    except YAMLFileError, e:
      print(color('red', e))
      sys.exit(1)

  # Get all roles and setup user config in ansible.cfg
  elif cli.sub_cmd == 'deploy':

    roles = Role(cli.env)
    print(color('cyan', '+ Fetching roles...'))
    try:
      roles.fetch('--force') if cli.force else roles.fetch()
      print(color('cyan', " {0} Done.".format(TICK)))
    except RoleError, e:
      print(color('red', "{0} {1}".format(CROSS, e.message)))
      sys.exit(1)

    ansible_cfg = AnsibleConfig(
        user_config_data['ansible_config'], inventory_file=control_repo.inventory_file, env=cli.env)
    ansible_cfg.create()
    print(color('cyan', "You are now working on '{0}'".format(cli.env)))

  else:
    parser.print_help()
