from .tag import Tag
from datetime import time

class Site:

	def __init__(self, site_dict):
		self._url = site_dict['url']
		self._interval = site_dict['interval']
		self._start_time_notification = self._get_time_from_str(site_dict['start_time_notification'])
		self._end_time = self._get_time_from_str(site_dict['end_time_notification'])
		self._tag = Tag(site_dict['tag'])
		self._keys = site_dict['keys']

	def get_url(self):
		return self._url

	def get_interval(self):
		return self._interval

	def get_start_time_notification(self):
		return self._start_time_notification

	def get_end_time_notification(self):
		return self._end_time

	def get_tag(self):
		return self._tag

	def get_keys(self):
		return self._keys

	def _get_time_from_str(self, time_str):
		splitted_time = time_str.split(":")
		return time(int(splitted_time[0]), int(splitted_time[1]))
