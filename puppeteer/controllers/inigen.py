"""Ansible Configuration File Manager"""

from config import YAMLFile, YAMLFileError
import ConfigParser


class AnsibleConfigError(Exception):
  """An exception that occurs when creating ansible.cfg file"""
  pass


class AnsibleConfig():

  def __init__(self, data, env):

    self.ansible_cfg_file = 'ansible.cfg'
    self.ansible_inventory_file = 'inventory.ini'
    self.ansible_roles_path = "environments/{0}/roles".format(env)
    self.ansible_inventory = "environments/{0}/{1}".format(
        env, self.ansible_inventory_file)

    try:
      self.config = data['ansible_config']
    except KeyError, e:
      # If no user config is provided initialize to empty
      self.config = None

  def create_ini(self):
    """Generate ansible.cfg file"""

    config = ConfigParser.ConfigParser()
    cfg_file = open(self.ansible_cfg_file, 'w')

    if self.config is not None:
      config.add_section('defaults')
      # Add path to inventory file in target environment
      config.set('defaults', 'inventory', self.ansible_inventory)
      if 'roles_path' not in self.config:
        config.set('defaults', 'roles_path', self.ansible_roles_path)

        for section in self.config.keys():
          for key, val in self.config[section].iteritems():

            if section == 'defaults':

              # Append existing roles path to prescribed roles path.
              if key == 'roles_path' and (val is not None):
                val = "{0}:{1}".format(self.ansible_roles_path, val)
            else:
              config.add_section(section)

            config.set(section, key, val)

          # Write entry to file
          config.write(cfg_file)

    # If no user config is provided, set defaults
    else:
      self._set_defaults(config, cfg_file)
      section = 'defaults'
      config.add_section(section)
      config.set(section, 'roles_path', self.ansible_roles_path)
      config.set(section, 'inventory', self.ansible_inventory)
      config.write(cfg_file)
    cfg_file.close()
