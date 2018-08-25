"""Application behaviour"""

import sys
from time import sleep
import cmdopts
from colourize import color
from fileops import YAMLFile, YAMLFileError
from controllers.controlrepo import ControlRepo, ControlRepoError
from controllers.inigen import AnsibleConfig, AnsibleConfigError
from controllers.role import Role, RoleError
from constants import USER_CONFIG, REPO_FILE, CROSS, TICK


def run():

  try:
    user_config = YAMLFile(USER_CONFIG).read()
  except YAMLFileError, e:
    print(color('red', "{0} {1}".format(CROSS, e)))
    print(color(
        'pink', 'File must be created if you are running puppeteer for the first time.'))

    sys.exit(1)

  parser = cmdopts.main(user_config['environments'])
  cli = parser.parse_args()

  # Initialize repository
  if cli.sub_cmd == 'init':

    try:
      control_repo = ControlRepo(user_config)
      print(color('cyan', '+ Initializing environments..'))
      control_repo.create_layout()
      sleep(0.4)
      print(color('cyan', "{0} Done.".format(TICK)))

    except ControlRepoError, e:
      print(color('red', e))
      sys.exit(1)

  elif cli.sub_cmd == 'show-config':

    ansible_cfg = AnsibleConfig(user_config)
    print(ansible_cfg.show())

  # Setup user config in ansible.cfg
  elif cli.sub_cmd == 'set-config':

    ansible_cfg = AnsibleConfig(user_config, cli.env)
    ansible_cfg.create()

  # List all roles
  elif cli.sub_cmd == 'list-roles':
    role = Role(cli.env)
    print(color('blue', role.list_roles()))

    # Get all roles
  elif cli.sub_cmd == 'get-roles':
    pass

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
