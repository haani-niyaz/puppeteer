"""Application behaviour"""

import sys
from fileops import YAMLFile, YAMLFileError
import cmdopts
from controllers.controlrepo import ControlRepo, ControlRepoError
from controllers.inigen import AnsibleConfig, AnsibleConfigError
from controllers.role import Role, RoleError
from colourize import color
from time import sleep

USER_CONFIG = '.puppeteer.yml'
REQUIREMENTS = 'requirements.yml'
CROSS = u'\u2717'.encode('utf8')
TICK = u'\u2713'.encode('utf8')


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

    try:
      req_file = "environments/{0}/{1}".format(cli.env, REQUIREMENTS)
      content = YAMLFile(req_file)
      print(content.show())

    except YAMLFileError, e:
      print(color('red', e))
      print(
          color('red', "{0} Cannot access '{1}' file.".format(CROSS, req_file)))
      sys.exit(1)

  # Tag a role
  elif cli.sub_cmd == 'tag-role':

    try:
      req_file = "environments/{0}/{1}".format(cli.env, REQUIREMENTS)
      content = YAMLFile(req_file)
      repo_data = content.read()

    except YAMLFileError, e:
      print(color('red', e))
      print(
          color('red', "{0} Cannot access '{1}' file.".format(CROSS, req_file)))
      sys.exit(1)

    try:
      role = Role(repo_data)
      updated_repo_data = role.tag(cli.name, cli.tag)
    except RoleError, e:
      if e.ec == RoleError.EXISTS:
        print(color('yellow', e.message))
        sys.exit(0)
      else:
        print(color('red', "{0} {1}".format(CROSS, e.message)))
        sys.exit(1)

    try:
      content.write(updated_repo_data)
      print(color('cyan', '+ Updating..'))
      print(color('green', role.confirm_tag(cli.name)))
      sleep(0.4)
      print(color('cyan', " {0} Done.".format(TICK)))
    except YAMLFileError, e:
      print(color('red', e))
      sys.exit(1)

  else:
    parser.print_help()


if __name__ == '__main__':
  run()
