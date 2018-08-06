"""Load and validate YAML files"""

import os
import yaml

USER_CONFIG='.puppeteer.yml'


class YAMLFileReaderError(Exception):
	"""An exception that occurs when a config file fails to load"""
	pass


class YAMLFileReader():
	"""Read YAML files"""

	def __init__(self):
		self.infile = USER_CONFIG


	def _validate_path(self):
		
		if not os.path.exists(self.infile):
			raise YAMLFileReaderError("User config file '%s' does not exist in current directory. File must be created if you are running puppeteer for the first time." % self.infile )


	def read(self): 

		self._validate_path()

		try:
			with open(self.infile, 'r') as stream:
				return yaml.load(stream)
		except yaml.YAMLError as e:
			if hasattr(e, 'problem_mark'):
				mark = e.problem_mark
				raise YAMLFileReaderError("%s has errors in position in line %s, column %s" % (self.infile,mark.line+1, mark.column+1))
			else:
				raise YAMLFileReaderError("Something went wrong while attempting to read %s" % self.infile )
