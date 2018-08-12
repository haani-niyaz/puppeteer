"""Application behaviour"""

import sys
from config import YAMLFile, YAMLFileError
import cmd_options
from controllers.bootstrap import BootstrapController, BootstrapControllerError
from controllers.tag import Tag, TagError
from colourize import color
from time import sleep

USER_CONFIG='.puppeteer.yml'
REQUIREMENTS='requirements.yml'

def main():

	cli = cmd_options.main()

	# Initialize repository
	if cli.sub_cmd == 'init':

		try:
			user_config = YAMLFile(USER_CONFIG).read()
		except YAMLFileError, e:
			print(color('red',e))
			print(color('red', "<Puppeteer> : File must be created if you are running puppeteer for the first time"))
			sys.exit(1)
		try:
			
			bootstrap = BootstrapController(user_config)
			print(color('cyan','[ ] Initializing environments..'))
			bootstrap.create_layout()
			sleep(0.4)
			print(color('cyan','[x] Done.'))

		except BootstrapControllerError, e:
			print(color('red',e))
			sys.exit(1)

	elif cli.sub_cmd == 'tag':

		try:
			req_file = "environments/{0}/{1}".format(cli.env,REQUIREMENTS)
			content = YAMLFile(req_file)
			repo_list = content.read()

		except YAMLFileError, e:
			print(color('red',e))
			print(color('red', "<Puppeteer> : Cannot access '{0}' file.".format(req_file)))
			sys.exit(1)

		try:
			tag = Tag(repo_list)
			updated_repo_list = tag.retag_repo(cli.role, cli.version)
		except TagError, e:
			if e.ec == TagError.EXISTS:
				print(color('yellow',e.message))
				sys.exit(0)
			else:
				print(color('red',e.message))
				sys.exit(1)

		try:
			content.write(updated_repo_list)
			print(color('cyan','[ ] Updating tag..'))
			print(color('green', tag.confirm_tag(cli.role)))
			sleep(0.4)
			print(color('cyan','[x] Done.'))
		except YAMLFileError, e:
			print(color('red',e))
			sys.exit(1)

