"""Orchestrate bootstrap tasks"""

class YAMLFileReaderError(Exception):
	"""An exception that occurs when Bootstrapping a repo"""
	pass


class BootstrapController():
	"""Control repo initialization"""

	def __init__(self, config):
		self.config = config

	def create_environments(self):
		"""Create control repo environments"""
		pass

	def create_requirements(self):
		"""Create requirements.yml"""
		pass

	def summary(self):
		"""Bootstrap summary"""
		pass