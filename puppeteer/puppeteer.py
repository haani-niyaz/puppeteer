"""Application behaviour"""

from config import YAMLFileReader, YAMLFileReaderError
import cmd_options
from controllers.bootstrap import BootstrapController

def main():

	cli = cmd_options.main()

	try:
		user_config = YAMLFileReader().read()
	except YAMLFileReaderError, e:
		print(color('red',e))
		sys.exit(1)

	# Initialize repository
	if cli.sub_cmd == 'init':

		try:
			bootstrap = BootstrapController(user_config)
			bootstrap.create_layout()
		except BootstrapControllerError, e:
			print(color('red',e))
			sys.exit(1)

	elif cli.sub_cmd == 'tag':
		print('do tag stuff')
