import argparse
import textwrap
from puppeteer import __version__ as VERSION


def main(envs):
  '''cli options'''

  parser = argparse.ArgumentParser(
      prog='puppeteer',
      description='Utility to manage Ansible workflow')

  parser.add_argument('-v', '--version', action='version',
                      version='%(prog)s {version}'.format(version=VERSION))

  subparsers = parser.add_subparsers(
      dest='sub_cmd', title='sub commands', help='-h, --help', metavar='[sub-command]')

  # Tag a role
  parser_tag_role = subparsers.add_parser(
      'tag-role',
      formatter_class=argparse.RawDescriptionHelpFormatter,
      help="update version in requirements.yml file",
      description=textwrap.dedent('''example:
  # update role 'jenkins' in requirements.yml with version '2.0.0' for the 'dev' environment
  puppeteer tag-role jenkins -e dev -t 2.0.0
      '''))
  parser_tag_role.add_argument('name', help='name of role')
  parser_tag_role_required = parser_tag_role.add_argument_group(
      'required arguments')
  parser_tag_role_required.add_argument('-t', '--tag',
                                        help='tag a role with a version')
  parser_tag_role_required.add_argument('-e', '--env', choices=envs+['all'],
                                        help='target environment')

  # Develop a role
  parser_develop_role = subparsers.add_parser(
      'dev-role',
      formatter_class=argparse.RawDescriptionHelpFormatter,
      help='develop and test role locally against a target environment',
      description=textwrap.dedent('''examples:
  
  # initialize skeleton role 'jenkins' in basedir '/var/tmp/role-workspace'
  puppeteer dev-role -s jenkins -w /var/tmp/roles
 
  # initialize skeleton role 'jenkins' in basedir '/var/tmp/role-workspace'
  # symlink from 'environments/dev/roles/jenkins' to '/var/tmp/role-workspace'
  puppeteer dev-role jenkins -w /var/tmp/roles -e dev
      '''))
  parser_develop_role.add_argument('name', help='name of role')
  parser_develop_role.add_argument('-s', '--setup', action='store_true',
                                   help='only setup role in development workspace')
  parser_develop_role_required = parser_develop_role.add_argument_group(
      'required arguments')
  parser_develop_role_required.add_argument('-w', '--workspace', required=True,
                                            help='path to workspace')
  parser_develop_role_required.add_argument('-e', '--env', choices=envs, required=True,
                                            help='symlink to workspace')

  # List roles
  parser_list_roles = subparsers.add_parser(
      'list-roles',
      help='list all roles requirements.yml file')
  parser_list_roles_required = parser_list_roles.add_argument_group(
      'required arguments')
  parser_list_roles_required.add_argument(
      'env', choices=envs, help='target environment')

  # Fetch roles
  parser_fetch_roles = subparsers.add_parser(
      'fetch-roles',
      help='fetch roles')
  parser_fetch_roles.add_argument(
      '-f', '--force', action='store_true', help='force overwrite an existing role')
  parser_fetch_roles.add_argument(
      'env', choices=envs, help='target environment')

  # Setup new project
  parser_new = subparsers.add_parser(
      'init',
      help='generate layout for a new project or reinitialize an existing project')

  # Apply user config to ansible.cfg
  parser_set_config = subparsers.add_parser(
      'set-config',
      help='generate ansible.cfg file')
  parser_set_config_required = parser_set_config.add_argument_group(
      'required arguments')
  parser_set_config_required.add_argument(
      'env', choices=envs, help='target environment')

  parser_show_config = subparsers.add_parser(
      'show-config',
      help='show ansible.cfg file')

  # Deploy
  parser_deploy = subparsers.add_parser(
      'deploy',
      help='all in one action to fetch roles and generate ansible.cfg file')
  parser_deploy.add_argument(
      'env', choices=envs, help='target environment')
  parser_deploy.add_argument(
      '-f', '--force', action='store_true', help='force overwrite an existing role')

  return parser
