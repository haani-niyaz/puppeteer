"""Application behaviour"""

from config import YAMLFileReader, YAMLFileReaderError

def main():

	try:
		user_config = YAMLFileReader().read()
		print (user_config)
	except YAMLFileReaderError, e:
		print(e)


if __name__ == '__main__':
	pass
	
