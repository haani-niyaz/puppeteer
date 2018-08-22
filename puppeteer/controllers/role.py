import os
import yaml


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


class Role:

  def __init__(self, data):

    if data is not None:
      self.repos = data
    else:
      raise RoleError('Requirements file cannot be empty')

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
