"""Orchestrate ControlRepo tasks"""

from utils import admin_tasks
from colourize import color
import sys


class ControlRepoError(Exception):
  """An exception that occurs when ControlRepoping a repo"""
  pass


class ControlRepo():
  """Control repo initialization"""

  def __init__(self, data):

    try:
      self.dirs = data['environments']
    except KeyError, e:
      raise ControlRepoControllerError(
          'Oops! does your .puppeteer.yml have a list of environments?')

    self.env_dir = 'environments'
    self.group_dir = 'group_vars'
    self.host_dir = 'host_vars'
    self.repo_file = 'requirements.yml'
    self.inventory_file = 'inventory.ini'

  def create_layout(self):
    """Create control repo layout"""

    try:
      for sub_dir in self.dirs:

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

  def summary(self):
    """ControlRepo summary"""
    pass
