import argparse
import textwrap


def main(envs):

  parser = argparse.ArgumentParser(
      prog='puppeteer',
      description='Utility to manage ansible workflow')

  subparsers = parser.add_subparsers(dest='sub_cmd', help='sub-command help')

  # Role operations
  parser_role = subparsers.add_parser(
      'role',
      formatter_class=argparse.RawDescriptionHelpFormatter,
      help='role specific actions',
      description=textwrap.dedent('''example:

  # Tag role jenkins in dev environment requirements.yml with version 2.0.0
  puppeteer role jenkins -e dev -t 2.0.0
      '''))
  parser_role.add_argument('-t', '--tag',
                           help='tag a role with a version')
  parser_role.add_argument('name', help='name of role')
  parser_role.add_argument('-e', '--env', choices=envs,
                           help='target environment')

  # Setup new project
  parser_new = subparsers.add_parser(
      'new',
      help='generate layout for a new project')

  # Apply user config to ansible.cfg
  parser_gen = subparsers.add_parser(
      'config',
      help='generate ansible.cfg file')
  parser_gen.add_argument('env', choices=envs, help='target environment')
  parser_gen.add_argument('-s', '--set', action='store_true', default=False,
                          help='set environment')

  return parser
