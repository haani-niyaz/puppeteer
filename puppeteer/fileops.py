import os
import yaml


class FileOps(object):

  def __init__(self, path):
    """Set path to file

    Args:
        path (str): file path
    """
    self._infile = path

  def _validate_path(self):
    """Validate path to file

    Raises:
        YAMLFileError: notify user that the file does not exist
    """
    if not os.path.exists(self._infile):
      raise YAMLFileError(
          "'{0}' does not exist".format(self._infile))

  def show(self):
    """Show contents of file

    Returns:
        str: returns contents of file
    """
    self._validate_path()
    with open(self._infile, 'r') as stream:
      return stream.read()

  def is_empty(self):
    """return True if self.read() is None else False"""
    self.read()


class YAMLFileError(Exception):
  """An exception that occurs when YAML file cannot load or has errors"""
  pass


class YAMLFile(FileOps):
  """Load, validate, write and show YAML files"""

  def __init__(self, path):
    """Set path to file

    Args:
        path (str): file path
    """
    super(YAMLFile, self).__init__(path)

  def _marker(self, error):
    """Helper to get yaml error positions in file

    Args:
        error (yaml.scanner.ScannerError):  scannerError object from exception raised

    Returns:
        str: Error message string
    """
    if hasattr(error, 'problem_mark'):
      mark = error.problem_mark
      return "{0} has errors in position in line {1}, column {2}".format(
          self._infile, mark.line+1, mark.column+1)
    else:
      return "Something went wrong while attempting to read {0}".format(self._infile)

  def read(self):
    """Read yaml file

    Returns:
        dict: contents of yaml file as a dictionary object

    Raises:
        YAMLFileError: notify user that the file has errors
    """
    super(YAMLFile, self)._validate_path()

    try:
      with open(self._infile, 'r') as stream:
        return yaml.load(stream, Loader=yaml.FullLoader)
    except yaml.scanner.ScannerError, e:
      raise YAMLFileError(self._marker(e))
    except yaml.YAMLError, e:
      raise YAMLFileError(self._marker(e))

  def write(self, data):
    """Write to yaml file

    Args:
        data (dict): dictionary of contents to write to file
    """
    with open(self._infile, 'w') as outfile:
      yaml.dump(data, outfile, default_flow_style=False)
