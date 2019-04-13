import sys
from time import sleep
from ..colourize import color
from ..fileops import FileOps, YAMLFile, YAMLFileError
# from ..actions.controlrepo import ControlRepo, ControlRepoError
# from ..actions.inigen import AnsibleConfig
from ..actions.role import Role, RoleError
from ..constants import USER_CONFIG_FILE, ANSIBLE_CONFIG_FILE, PROJECT_URL, CROSS, TICK


def execute_tag_role(name='', tag='', env=''):

  try:
    role = Role(env)
    updated_repo_data = role.tag(name, tag)
  except RoleError, e:
    if e.ec == RoleError.EXISTS:
      print(color('yellow', e.message + 'in {0}'.format(env)))
      sys.exit(0)
    else:
      print(color('red', "{0} {1}".format(CROSS, e.message)))
      sys.exit(1)

  try:
    role.update_repo_file(updated_repo_data)
    print(color('cyan', '+ Updating {0} environment..'.format(env)))
    print(color('green', role.confirm_tag(name)))
    sleep(0.4)
    print(color('cyan', " {0} Done.".format(TICK)))
  except YAMLFileError, e:
    print(color('red', e))
    sys.exit(1)


def execute_fetch_roles(env, force):
  roles = Role(env)
  print(color('cyan', '+ Fetching roles...'))
  try:
    roles.fetch('--force') if force else roles.fetch()
    print(color('cyan', " {0} Done.".format(TICK)))
  except RoleError, e:
    print(color('red', "{0} {1}".format(CROSS, e.message)))
    sys.exit(1)
