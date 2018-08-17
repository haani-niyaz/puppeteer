import argparse


def main(envs):

  parser = argparse.ArgumentParser(
      prog='puppeteer', description='Utility to manage ansible workflow')

  subparsers = parser.add_subparsers(dest='sub_cmd', help='sub-command help')

  # Tag operations
  parser_tag = subparsers.add_parser(
      'role', help='role specific actions')
  parser_tag.add_argument('-t', '--tag',
                          help='tag a role with a version')
  parser_tag.add_argument('name', help='name of role')
  parser_tag.add_argument('-e', '--env', choices=envs,
                          help='target environment')

  # Setup new project
  parser_new = subparsers.add_parser(
      'new', help='generate layout for a new project')

  # Apply user config to ansible.cfg
  parser_setup = subparsers.add_parser(
      'gen', help='generate ansible.cfg file')
  parser_setup.add_argument('env', choices=envs, help='target environment')

  return parser
