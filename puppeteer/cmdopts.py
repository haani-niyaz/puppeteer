import argparse
import textwrap


def main(envs):

  parser = argparse.ArgumentParser(
      prog='puppeteer',
      description='Utility to manage ansible workflow')

  subparsers = parser.add_subparsers(dest='sub_cmd', help='sub-command help')

  # Role operations
  parser_tag_role = subparsers.add_parser(
      'tag-role',
      formatter_class=argparse.RawDescriptionHelpFormatter,
      help='tag a role in repo file',
      description=textwrap.dedent('''example:

  # Tag role jenkins in dev environment requirements.yml with version 2.0.0
  puppeteer role jenkins -e dev -t 2.0.0
      '''))
  parser_tag_role.add_argument('-t', '--tag',
                               help='tag a role with a version')
  parser_tag_role.add_argument('name', help='name of role')
  parser_tag_role.add_argument('-e', '--env', choices=envs,
                               help='target environment')

  # Apply user config to ansible.cfg
  parser_list_roles = subparsers.add_parser(
      'list-roles',
      help='list roles in repo file')
  parser_list_roles.add_argument(
      'env', choices=envs, help='target environment')

  # Setup new project
  parser_new = subparsers.add_parser(
      'init',
      help='generate layout for a new project')

  # Apply user config to ansible.cfg
  parser_set_config = subparsers.add_parser(
      'set-config',
      help='generate ansible.cfg file')
  parser_set_config.add_argument(
      'env', choices=envs, help='target environment')

  parser_show_config = subparsers.add_parser(
      'show-config',
      help='show ansible.cfg file')

  return parser
