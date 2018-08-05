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