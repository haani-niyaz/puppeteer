"""Application behaviour"""

import sys
from fileops import YAMLFile, YAMLFileError
import cmdopts
from controllers.bootstrap import Bootstrap, BootstrapError
from controllers.inigen import AnsibleConfig, AnsibleConfigError
from controllers.tag import Tag, TagError
from colourize import color
from time import sleep

USER_CONFIG = '.puppeteer.yml'
REQUIREMENTS = 'requirements.yml'
CROSS = u'\u2717'.encode('utf8')
TICK = u'\u2713'.encode('utf8')


def run():

  try:
    user_config = YAMLFile(USER_CONFIG).read()
  except YAMLFileError, e:
    print(color('red', "{0} {1}".format(CROSS, e)))
    print(color(
        'pink', 'File must be created if you are running puppeteer for the first time.'))
    sys.exit(1)

  parser = cmdopts.main(user_config['environments'])
  cli = parser.parse_args()

  # Initialize repository
  if cli.sub_cmd == 'new':

    try:
      bootstrap = Bootstrap(user_config)
      print(color('cyan', '+ Initializing environments..'))
      bootstrap.create_layout()
      sleep(0.4)
      print(color('cyan', "{0} Done.".format(TICK)))

    except BootstrapError, e:
      print(color('red', e))
      sys.exit(1)

  # Setup user config in ansible.cfg
  elif cli.sub_cmd == 'gen':

    ansible_cfg = AnsibleConfig(user_config, cli.env)
    ansible_cfg.create_ini()

  # Tag a repo with a new version
  elif cli.sub_cmd == 'tag':

    try:
      req_file = "environments/{0}/{1}".format(cli.env, REQUIREMENTS)
      content = YAMLFile(req_file)
      repo_list = content.read()

    except YAMLFileError, e:
      print(color('red', e))
      print(
          color('red', "{0} Cannot access '{1}' file.".format(CROSS, req_file)))
      sys.exit(1)

    try:
      tag = Tag(repo_list)
      updated_repo_list = tag.retag_repo(cli.role, cli.version)
    except TagError, e:
      if e.ec == TagError.EXISTS:
        print(color('yellow', e.message))
        sys.exit(0)
      else:
        print(color('red', "{0} {1}".format(CROSS, e.message)))
        sys.exit(1)

    try:
      content.write(updated_repo_list)
      print(color('cyan', '+ Updating..'))
      print(color('green', tag.confirm_tag(cli.role)))
      sleep(0.4)
      print(color('cyan', " {0} Done.".format(TICK)))
    except YAMLFileError, e:
      print(color('red', e))
      sys.exit(1)


if __name__ == '__main__':
  run()
