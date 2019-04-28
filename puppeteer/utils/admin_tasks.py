"""System admin tasks"""

import os
import errno
import pwd
from subprocess import Popen, PIPE, check_output, CalledProcessError
import sys
import shutil


class AdminTasksError(Exception):
  """An exception that occurs when performing administrative operations"""
  pass


def make_dirs(dirs):
  """Create directories recursively"""

  if not dir_exists(dirs):
    try:
      os.makedirs(dirs)
    except OSError as e:
      raise AdminTasksError(
          "Directory '{0}' failed with error '{1}'".format(dirs, e))


def dir_exists(path):
  """Check the presence of a directory

  Args:
    path (str): path to dir

  Returns:
    boolean
  """
  return os.path.isdir(path)


def symlink_exists(path):
  """Check the presence of a symlink

  Args:
    path (str): path to dir

  Returns:
    boolean
  """

  return os.path.islink(path)


def remove_dir(path):
  """Remove directory in a given path"""

  if os.path.islink(path):
    os.unlink(path)

  if dir_exists(path):
    try:
      shutil.rmtree(path)
    except OSError as e:
      raise AdminTasksError(
          "Deleting {0} failed with error '{1}'".format(e.filename, e.strerror))


def symlink(src, link_name):
  """Create symlink"""

  os.symlink(src, link_name)


def make_file(infile):
  """Create a file if does not exist

  Args:
      infile (str): path to file

  Returns:
      str: notice to calling program that file already exists
  """

  if not os.path.exists(infile):
    with open(infile, 'w'):
      pass
  else:
    return("'{0}' file already exists".format(infile))


def run_cmd(cmd):
  """Run command and print output

  Args:
      cmd (str): unix command string

  Raises:
      AdminTasksError: validates if the 'command' to execute exists in the user's path
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
