"""Orchestrate ControlRepo tasks"""

import sys
from ..utils import admin_tasks
from ..constants import REPO_FILE


class ControlRepoError(Exception):
  """An exception that occurs when ControlRepoping a repo"""
  pass


class ControlRepo(object):
  """Control repo initialization"""

  def __init__(self, config):

    try:
      self.envs = config.get('environments')
      if self.envs is None or type(self.envs) is not list:
        raise ControlRepoError(
            '.puppeteer.yml must have a list of environments.')

    except TypeError as e:
      raise ControlRepoError(
          '.puppeteer.yml file must have a list of environments.')

    self.inventory_file = config.get('inventory_file_name', 'inventory.ini')
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
