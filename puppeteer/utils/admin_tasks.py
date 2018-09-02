
"""System admin tasks"""

import os
import errno
import pwd
from subprocess import Popen, PIPE, check_output, CalledProcessError
import sys


class AdminTasksError(Exception):
  """An exception that occurs when performing administrative operations"""
  pass


def make_dirs(dirs):
  """Create directories recursively if it does not exist

  Args:
      dirs (str): Path to directory. Sub-directories will be create if it does not exist

  Returns:
      str: Notice to calling program that directory already exists

  Raises:
      AdminTasksError: For any errors in the creation process notify calling program
  """

  try:
    os.makedirs(dirs)
  except OSError, e:
    if e.errno == errno.EEXIST:
      return("'{0}' directory already exists".format(dirs))
    else:
      raise AdminTasksError(
          "Backup directory creation failed with error {0}".format(str(e)))


def make_file(infile):
  """Create a file if does not exist

  Args:
      infile (str): Path to file

  Returns:
      str: Notice to calling program that file already exists
  """

  if not os.path.exists(infile):
    with open(infile, 'w'):
      pass
  else:
    return("'{0}' file already exists".format(infile))


def run_cmd(cmd):
  """Run command and print output 

  Args:
      cmd (str): Unix command string

  Raises:
      AdminTasksError: Validates if the 'command' to execute exists in the user's path
  """

  cmd = cmd.split()
  try:
    check_output(['which', cmd[0]])
  except CalledProcessError, e:
    raise AdminTasksError("Is '{0}' executable in your path?".format(cmd[0]))

  process = Popen(cmd, stdout=PIPE, stderr=PIPE)
  # Wait for child process to terminate before checking ext code
  process.wait()

  # Write to stdout if no failures
  if process.returncode == 0:
    [sys.stdout.write(line) for line in process.stdout]
  else:
    message = ''.join(process.stderr)
    raise AdminTasksError(message)
