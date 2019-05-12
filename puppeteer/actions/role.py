import sys
from ..fileops import YAMLFile, YAMLFileError
from ..constants import REPO_FILE, PUPPETEER_WORKSPACE, CROSS
from ..colourize import color
from ..utils.admin_tasks import run_cmd, AdminTasksError, dir_exists, remove_dir, symlink_exists, symlink, make_dirs


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
    """Initialize role object

    Args:
        env (str): target environment of requirements.yml

    Raises:
        RoleError: notify user of errors encoutered when reading requirements.yml
                   file
    """

    self.workspace = "{0}/roles".format(PUPPETEER_WORKSPACE)
    # Get repo data from requirements.yml
    self._req_file_path = "environments/{0}/{1}".format(env, REPO_FILE)
    self._requirements = YAMLFile(self._req_file_path)

    try:
      data = self._requirements.read()
    except YAMLFileError, e:
      raise RoleError(e)

    if data is not None:
      self.repos = data
    else:
      raise RoleError("'{}' file is empty".format(self._req_file_path))

    self.roles_path = "environments/{0}/roles".format(env)
    self.repo_fetcher = 'ansible-galaxy'

  def tag(self, name, version):
    """Update a role's tag in requirements.yml

    Args:
        name (str): role name
        version (str): version to set

    Returns:
        dict: updated requirements.yml for role tag

    Raises:
        RoleError: notify user if the version is already set
                   or role does not exist in requirements.yml
    """
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
    """Get tag for a role

    Args:
        name (str): role name

    Returns:
        tuple: role name and tag

    Raises:
        RoleError: Description
    """
    for repo in self.repos:
      if repo['name'] == name:
        return (repo['name'], repo['version'])

    raise RoleError('Something went wrong')

  def list_roles(self):
    """Show roles in requirements.yml

    Returns:
        str: contents of file
    """
    return self._requirements.show()

  def update_repo_file(self, data):
    """Update requirements.yml"""

    try:
      self._requirements.write(data)
    except YAMLFileError as e:
      raise RoleError(e)

  def fetch(self, option=None):
    """Get ansible roles in requirements.yml

    Args:
        option (None, optional): option to force overwrite roles already downloaded

    Raises:
        RoleError: notify user of any errors encountered when the ansible-galaxy
                   command is run
    """
    default_cmd = "ansible-galaxy install -p {0} -r {1}".format(
        self.roles_path, self._req_file_path)

    try:
      if option:
        run_cmd("{0} {1}".format(default_cmd, option))
      else:
        run_cmd(default_cmd)
    except AdminTasksError, e:
      raise RoleError(e)

  def _create_workspace(self):
    """Create default workspace"""

    try:
      make_dirs(self.workspace)
    except AdminTasksError as e:
      raise RoleError(e)

  def symlink_local_role(self, role_name, workspace=None):
    """Symlink environments/{env}/roles/{role_name} to workspace {basedir}/{role_name}

    Args:
      role_name (str): Name of role
      workspace (str): Base directory for local role 
    """

    if not workspace:
      self._create_workspace()
    else:
      self.workspace = workspace

    local_role_path = "{0}/{1}".format(self.workspace, role_name)
    environment_role_path = "{0}/{1}".format(self.roles_path, role_name)

    if dir_exists(local_role_path):
      # Remove environments/{env}/roles/{role_name} dir
      try:
        remove_dir(environment_role_path)
      except AdminTasksError as e:
        raise RoleError(e)

      # Symlink environments/{env}/roles/{role_name} to workspace {basedir}/{role_name}
      symlink(local_role_path, environment_role_path)
    else:
      raise RoleError(
          "Development role '{0}' does not exist".format(local_role_path))

  def unsymlink_local_role(self, role_name):
    """Remove symlink environments/{env}/roles/{role_name} to workspace {basedir}/{role_name}

    Args:
      role_name (str): Name of role
    """

    environment_role_path = "{0}/{1}".format(self.roles_path, role_name)
    if not symlink_exists(environment_role_path):
      raise RoleError('Symlink already removed', RoleError.EXISTS)

    remove_dir(environment_role_path)
