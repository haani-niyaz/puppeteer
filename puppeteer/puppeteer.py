"""Application behaviour"""

from config import YAMLFileReader, YAMLFileReaderError
import cmd_options
from controllers.bootstrap import BootstrapController

def main():

	cli = cmd_options.main()

	try:
		user_config = YAMLFileReader().read()
		# Debug
		print (user_config)	
	except YAMLFileReaderError, e:
		print(e)

	if cli.sub_cmd == 'init':
		print('do init stuff')
		bootstrap = BootstrapController(user_config)

	elif cli.sub_cmd == 'tag':
		print('do tag stuff')
