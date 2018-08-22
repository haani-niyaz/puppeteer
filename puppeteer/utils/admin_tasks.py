
"""System admin tasks"""

import os
import errno
import pwd
from subprocess import check_output, CalledProcessError, STDOUT


class AdminTasksError(Exception):
  """An exception that occurs when performing administrative operations"""
  pass


def make_dirs(dirs):
  """Create directories recursively if it does not exist"""

  try:
    os.makedirs(dirs)
  except OSError, e:
    if e.errno == errno.EEXIST:
      return("'{0}' directory already exists".format(dirs))
    else:
      raise AdminTasksError(
          "Backup directory creation failed with error {0}".format(str(e)))


def make_file(infile):
  """Create a file if does not exist"""

  if not os.path.exists(infile):
    with open(infile, 'w'):
      pass
  else:
    return("'{0}' file already exists".format(infile))


def run_cmd(cmd):

  try:
    check_output(
        cmd, stderr=STDOUT)
  except CalledProcessError, e:
    print(e.output)
