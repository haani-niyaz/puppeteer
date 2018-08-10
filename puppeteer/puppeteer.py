"""Application behaviour"""

import sys
from config import YAMLFileReader, YAMLFileReaderError
import cmd_options
from controllers.bootstrap import BootstrapController, BootstrapControllerError
from controllers.tag import Tag, TagError
from colourize import color

USER_CONFIG='.puppeteer.yml'


def main():

	cli = cmd_options.main()

	# Initialize repository
	if cli.sub_cmd == 'init':

		try:
			user_config = YAMLFileReader(USER_CONFIG).read()
		except YAMLFileReaderError, e:
			print(color('red',e))
			print(color('red', "<Puppeteer> : File must be created if you are running puppeteer for the first time"))
			sys.exit(1)
		try:
			bootstrap = BootstrapController(user_config)
			bootstrap.create_layout()
		except BootstrapControllerError, e:
			print(color('red',e))
			sys.exit(1)
