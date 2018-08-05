"""Application behaviour"""

from config import YAMLFileReader, YAMLFileReaderError
import cmd_options

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

	elif cli.sub_cmd == 'tag':
		print('do tag stuff')
