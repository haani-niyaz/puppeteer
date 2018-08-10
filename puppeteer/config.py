"""Load and validate YAML files"""

import os
import yaml


class YAMLFileError(Exception):
	"""An exception that occurs when a config file fails to load"""
	pass


class YAMLFile():
	"""Read YAML files"""

	def __init__(self, path):
		self.infile = path


	def _validate_path(self):
		
		if not os.path.exists(self.infile):
			raise YAMLFile("User config file '%s' does not exist in current directory." % self.infile )


	def read(self): 

		self._validate_path()

		try:
			with open(self.infile, 'r') as stream:
				return yaml.load(stream)
		except yaml.YAMLError as e:
			if hasattr(e, 'problem_mark'):
				mark = e.problem_mark
				raise YAMLFile("%s has errors in position in line %s, column %s" % (self.infile,mark.line+1, mark.column+1))
			else:
				raise YAMLFile("Something went wrong while attempting to read %s" % self.infile )

	def write(self,data):

		with open(self.infile, 'w') as outfile:
			yaml.dump(data, outfile, default_flow_style=False)			