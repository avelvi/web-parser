from urllib.parse import urlparse
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

from config.config import Config
from dto.data_dto import DataDto
from entity.site import Site
from notification.email_notification import EmailNotification
from scheduler.scheduler import Scheduler
from logger.logger import logger
from helpers.time import now_datetime


class Parser:

	def __init__(self, config: Config):
		self._scheduler = Scheduler()
		self._email_notification = EmailNotification(config.get('smtp'), config.get('recipients'))
		for site in config.get('sites'):

			self._scheduler.every_minutes(Site(site), self.parse)
		logger.info(f"Will be parsing {len(config.get('sites'))} site(s)")

	def parse(self, site: Site):
		result = urlparse(site.get_url())
		url = f'{result.scheme}://{result.netloc}'
		if not all([result.scheme, result.netloc, result.path]):
			logger.warn(f'Something wrong with url - {url}')
			return False
		logger.info(f'Parsing data for {url}')
		req = Request(site.get_url(), headers={'User-Agent': 'Mozilla/5.0'})
		page = urlopen(req).read()
		soup = BeautifulSoup(page, 'html.parser')
		selector = site.get_tag().get_selector()
		items = soup.select(selector)

		data = []
		for item in items:
			tmp_text = item.get_text().strip().split('\n')[0].lower()
			if any(key in tmp_text for key in site.get_keys()):
				text = item.get_text().strip().replace('\n', ' ')
				href = item.get('href')
				data.append(DataDto(text, href))

		if len(data) > 0:
			if self._check_time_range(site.get_start_time_notification(), site.get_end_time_notification()):
				self._email_notification.send_email(f'{result.scheme}://{result.netloc}', data)
			else:
				logger.info(f'Found {len(data)} records for {url}')
				logger.info('Current time not in time ranges')
		return True

	def _check_time_range(self, start_time, end_time):
		return True if start_time < now_datetime().time() < end_time else False

	def run(self):
		self._scheduler.run()
