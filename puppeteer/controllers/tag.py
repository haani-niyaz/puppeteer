import os
import yaml


class TagError(Exception):
  """An exception that occurs when setting the tag in requirements.yml"""

  EXISTS = 130

  def __init__(self, message, exit_code=1, *args):
    self.message = message  # without this you may get DeprecationWarning
    # Special attribute you desire with your Error,
    # perhaps the value that caused the error?:
    self.ec = exit_code
    # allow users initialize misc. arguments as any other builtin Error
    super(TagError, self).__init__(message, exit_code, *args)


class Tag:

  def __init__(self, data):

    if data is not None:
      self.data = data
    else:
      raise TagError('Requirements file cannot be empty')

  def retag_repo(self, name, version):

    for repo in self.data:
      if repo['name'] == name:
        if repo['version'] == version:
          raise TagError("Version is already set to '%s'" %
                         str(repo['version']), TagError.EXISTS)
        else:
          repo['version'] = version
          return self.data

    raise TagError("Role '%s' does not exist" % name)

  def confirm_tag(self, name):

    for repo in self.data:
      if repo['name'] == name:
        return (repo['name'], repo['version'])

    raise TagError('Something went wrong')
