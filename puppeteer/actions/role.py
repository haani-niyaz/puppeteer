import sys
from ..fileops import YAMLFile, YAMLFileError
from ..constants import REPO_FILE, CROSS
from ..colourize import color
from ..utils.admin_tasks import run_cmd, AdminTasksError


class RoleError(Exception):
  """An exception that occurs when action is performed on a role"""

  EXISTS = 130

  def __init__(self, message, exit_code=1, *args):
    self.message = message  # without this you may get DeprecationWarning
    # Special attribute you desire with your Error,
    # perhaps the value that caused the error?:
    self.ec = exit_code
    # allow users initialize misc. arguments as any other builtin Error
    super(RoleError, self).__init__(message, exit_code, *args)


class Role(object):

  def __init__(self, env):

    # Get repo data from requirements.yml
    self.req_file = "environments/{0}/{1}".format(env, REPO_FILE)
    self.requirements = YAMLFile(self.req_file)

    try:
      data = self.requirements.read()
    except YAMLFileError, e:
      print(
          color('red', "{0} {1}".format(CROSS, e)))
      sys.exit(1)

    if data is not None:
      self.repos = data
    else:
      raise RoleError('Requirements file cannot be empty')

    self.roles_path = "environments/{0}/roles".format(env)
    self.repo_fetcher = 'ansible-galaxy'

  def tag(self, name, version):

    for repo in self.repos:
      if repo['name'] == name:
        if repo['version'] == version:
          raise RoleError("Version is already set to '%s'" %
                          str(repo['version']), RoleError.EXISTS)
        else:
          repo['version'] = version
          return self.repos

    raise RoleError("Role '%s' does not exist" % name)

  def confirm_tag(self, name):

    for repo in self.repos:
      if repo['name'] == name:
        return (repo['name'], repo['version'])

    raise RoleError('Something went wrong')

  def list_roles(self):
    return self.requirements.show()

  def update_repo_file(self, data):
    self.requirements.write(data)

  def fetch(self, option=None):

    default_cmd = "ansible-galaxy install -p {0} -r {1}".format(
        self.roles_path, self.req_file)

    try:
      if option:
        run_cmd("{0} {1}".format(default_cmd, option))
      else:
        run_cmd(default_cmd)
    except AdminTasksError, e:
      raise RoleError(e)