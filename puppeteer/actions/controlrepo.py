"""Orchestrate ControlRepo tasks"""

import sys
from ..utils import admin_tasks
from ..constants import PROJECT_URL, REPO_FILE


class ControlRepoError(Exception):
  """An exception that occurs when ControlRepoping a repo"""
  pass


class ControlRepo(object):
  """Control repo initialization"""

  def __init__(self, config):
    """Initialize control repo object

    Args:
        config (config): Expects an object with the key 'environments' (list) and optionally
                         'inventory_file_name' (str)

    Raises:
        ControlRepoError: Raise an exception to the calling program if the following is met:
                          1. '.puppeteer.yml' does not have var 'environment' of sequence type (list) 
                             defined 
                          2. 'environments' var is empty
                          3. 'environments' var is not a list
    """
    err_message = ".puppeteer.yml must have a list of environments. Please see setup details at {0}.".format(
        PROJECT_URL)
    try:
      self.envs = config.get('environments')
      if self.envs is None or type(self.envs) is not list:
        raise ControlRepoError(err_message)
    except (TypeError, AttributeError) as e:
      raise ControlRepoError(err_message)

    self.inventory_file = config.get('inventory_file', 'inventory.ini')
    self.repo_file = REPO_FILE
    self.env_dir = 'environments'
    self.group_dir = 'group_vars'
    self.host_dir = 'host_vars'

  def create_layout(self):
    """Create control repo layout"""

    try:
      for sub_dir in self.envs:

        admin_tasks.make_dirs(
            "{0}/{1}/{2}".format(self.env_dir, sub_dir, self.group_dir))
        admin_tasks.make_dirs(
            "{0}/{1}/{2}".format(self.env_dir, sub_dir, self.host_dir))
        admin_tasks.make_file(
            "{0}/{1}/{2}".format(self.env_dir, sub_dir, self.repo_file))
        admin_tasks.make_file(
            "{0}/{1}/{2}".format(self.env_dir, sub_dir, self.inventory_file))

    except admin_tasks.AdminTasksError, e:
      print(e)
      sys.exit(1)
