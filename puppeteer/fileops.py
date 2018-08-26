"""File operations"""

import os
import yaml


class YAMLFileError(Exception):
  """An exception that occurs when a config file fails to load"""
  pass


class YAMLFile():
  """Load, validate, write and show YAML files"""

  def __init__(self, path):

    self.infile = path

  def _validate_path(self):

    if not os.path.exists(self.infile):
      raise YAMLFileError(
          "'{0}' does not exist in current directory.".format(self.infile))

  def read(self):

    self._validate_path()

    try:
      with open(self.infile, 'r') as stream:
        return yaml.load(stream)
    except yaml.YAMLError, e:
      if hasattr(e, 'problem_mark'):
        mark = e.problem_mark
        raise YAMLFileError("{0} has errors in position in line {1}, column {2}".format(
            self.infile, mark.line+1, mark.column+1))
      else:
        raise YAMLFileError(
            "Something went wrong while attempting to read %s" % self.infile)
    except yaml.scanner.ScannerError, e:
      raise YAMLFileError(e)

  def write(self, data):

    with open(self.infile, 'w') as outfile:
      yaml.dump(data, outfile, default_flow_style=False)

  def show(self):

    self._validate_path()
    with open(self.infile, 'r') as stream:
      return stream.read()

  def is_empty(self):

    # return True if self.read() is None else False
    self.read()
