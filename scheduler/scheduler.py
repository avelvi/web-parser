import asyncio
from entity.site import Site

TOTAL_SECONDS_IN_1_MINUTE = 60


class Scheduler:
	_loop = asyncio.get_event_loop()
	_when_completed = asyncio.Future()
	_counter = 0

	def every_minutes(self, site: Site, callback):
		self._counter += 1
		subscribed = [True]
		interval_in_seconds = site.get_interval() * TOTAL_SECONDS_IN_1_MINUTE

		def unsubscribe():
			subscribed[0] = False
			self._counter -= 1
			if self._counter <= 0:
				self._when_completed.set_result(True)

		def callback_wrapper():
			if not subscribed[0]:
				return
			self._loop.call_later(interval_in_seconds, callback_wrapper)
			callback(site)

		self._loop.call_later(interval_in_seconds, callback_wrapper)
		return unsubscribe

	def run(self):
		self._loop.run_until_complete(self._when_completed)

