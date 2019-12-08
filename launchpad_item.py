class LaunchpadItem:

	TYPE_ROOT = 1
	TYPE_GROUP = 2
	TYPE_PAGE = 3
	TYPE_APP = 4

	def __init__(self):
		self.type = None
		self.id = None
		self.uuid = None
		self.title = None
		self.parent = None
		self.children = []
		self.ordering = 0


