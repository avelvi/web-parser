import json
import os


class Config(object):
	_properties = None
	_env = 'default'

	def __init__(self):
		env_file_path = "./.env"
		if os.path.isfile(env_file_path):
			with open(env_file_path) as env_file:
				env = env_file.readline().strip('\t\n\r')
				if os.path.exists('./properties/%s.json' % env):
					self._env = env

	def parse(self):
		if Config._properties is None:
			with open('./properties/%s.json' % self._env) as property_file:
				Config._properties = json.load(property_file)

	def get(self, key):
		self.parse()
		return self._properties[key] if key in self._properties else None

	def get_properties(self):
		return self._properties
