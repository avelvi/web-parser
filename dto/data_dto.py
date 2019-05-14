class DataDto:
	def __init__(self, text, href):
		self._text = text
		self._href = href

	def get_text(self):
		return self._text

	def get_href(self):
		return self._href
