"""Ansible Configuration File Manager"""

from config import YAMLFile, YAMLFileError
import ConfigParser


class AnsibleConfigError(Exception):
  """An exception that occurs when creating ansible.cfg file"""
  pass


class AnsibleConfig():
  """ Generate ansible.cfg file"""

  def __init__(self, data, env=None):

    self.ansible_cfg_file = 'ansible.cfg'
    self.ansible_inventory_file = 'inventory.ini'
    self.ansible_roles_path = "environments/{0}/roles".format(env)
    self.ansible_inventory = "environments/{0}/{1}".format(
        env, self.ansible_inventory_file)

    try:
      self.user_config = data['ansible_config']
    except KeyError, e:
      # If no user config is provided initialize to empty
      self.user_config = None


# TO-DO:
# 1. If user_config is empty, provide defaults
# 2. If user_config has roles_path, append roles path [done]
# 3. If inventory path is supplised discard it

  def create(self):
    """Generate ansible.cfg file"""

    config = ConfigParser.ConfigParser()
    cfg_file = open(self.ansible_cfg_file, 'w')

    for section in self.user_config.keys():

      config.add_section(section)

      for key, val in self.user_config[section].iteritems():

        if section == 'defaults':

          # Add path to inventory file in target environment
          config.set(section, 'inventory', self.ansible_inventory)

          # Append existing roles path to prescribed roles path.
          if key == 'roles_path' and (val is not None):
            val = "{0}:{1}".format(self.ansible_roles_path, val)

        config.set(section, key, val)

    # Write to file
    config.write(cfg_file)

    cfg_file.close()

  def show(self):
    """Show ansible.cfg file"""

    with open(self.ansible_cfg_file, 'r') as stream:
      return stream.read()
