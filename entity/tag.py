class Tag:
	def __init__(self, tag_dict):
		self._name = tag_dict['name']
		self._clazz = tag_dict['clazz']
		child_tag = tag_dict['child_tag']
		self._child_tag = child_tag if not child_tag else Tag(child_tag)

	def get_name(self):
		return self._name

	def get_clazz(self):
		return self._clazz

	def get_child_tag(self):
		return self._child_tag

	def has_child_tag(self):
		return bool(self._child_tag)

	def get_selector(self):
		if self.has_child_tag():
			return "%s.%s %s" % (self._name, self._clazz, self.get_child_tag().get_selector())
		return "%s.%s" % (self._name, self._clazz)
