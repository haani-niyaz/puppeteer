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
      description=textwrap.dedent('''
  Update a role's version in requirements.yml file     

  Examples:
    # update role 'jenkins' in requirements.yml with version '2.0.0' in environment 'dev'
    puppeteer tag-role jenkins -t 2.0.0 -e dev 

    # update role 'jenkins' in requirements.yml with version '2.0.0' in all environments
    puppeteer tag-role jenkins -t 2.0.0 -e all
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
      description=textwrap.dedent('''
  Symlink from environment directory to role in a development workspace      

  Examples:
    # symlink from 'environments/dev/roles/jenkins' to default workspace '.puppeteer/roles/jenkins'
    puppeteer dev-role jenkins -e dev

    # symlink from 'environments/dev/roles/jenkins' to custom workspace '/var/tmp/role/jenkins'
    puppeteer dev-role jenkins --workspace /var/tmp/roles -e dev

    # remove symlink
    puppeteer dev-role jenkins -e dev --clean

      '''))
  parser_develop_role.add_argument('name', help='name of role')
  parser_develop_role.add_argument('-w', '--workspace',
                                   help='override default workspace ~/.puppeteer/roles')
  parser_develop_role.add_argument('-c', '--clean', action='store_true',
                                   help='remove symlink to role in workspace')
  parser_develop_role_required = parser_develop_role.add_argument_group(
      'required arguments')
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
