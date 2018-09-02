"""Application behaviour"""

import sys
from time import sleep
import cmdopts
from .colourize import color
from .fileops import YAMLFile, YAMLFileError
from .actions.controlrepo import ControlRepo, ControlRepoError
from .actions.inigen import AnsibleConfig
from .actions.role import Role, RoleError
from .constants import USER_CONFIG_FILE, CROSS, TICK


def main():

  # Parser relies on dynamically loading environments from the user cofig
  # so let's attempt to get the list of environments first
  try:
    user_config = YAMLFile(USER_CONFIG_FILE)
    user_config_data = user_config.read()

    try:
      # Initialize control repo
      control_repo = ControlRepo(user_config_data['control_repo'])
    except ControlRepoError as e:
      print(color('red', "{0} {1}".format(CROSS, e)))
      sys.exit(1)

  except YAMLFileError, e:
    print(color('red', "{0} {1}".format(CROSS, e)))
    sys.exit(1)

  # Initialize parser with environments
  parser = cmdopts.main(control_repo.envs)
  cli = parser.parse_args()

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

  elif cli.sub_cmd == 'show-config':

    ansible_cfg = AnsibleConfig(user_config_data['ansible_config'])
    print(ansible_cfg.show())

  # Setup user config in ansible.cfg
  elif cli.sub_cmd == 'set-config':

    ansible_cfg = AnsibleConfig(user_config_data['ansible_config'], cli.env)
    ansible_cfg.create()

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

  else:
    parser.print_help()
