import argparse


def main(envs):

  parser = argparse.ArgumentParser(
      prog='puppeteer', description='Utility to manage ansible workflow')

  subparsers = parser.add_subparsers(dest='sub_cmd', help='sub-command help')

  # Tag parser
  parser_tag = subparsers.add_parser(
      'tag', help='tag an environment specific repo with a new version')
  parser_tag.add_argument('version', help='new version')
  parser_tag.add_argument('-r', '--role', help='role name')
  parser_tag.add_argument('-e', '--env', choices=envs,
                          help='target environment')

  # Setup new project
  parser_new = subparsers.add_parser(
      'new', help='generate layout for a new project')

  return parser.parse_args()
