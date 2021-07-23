class SVGelement:
	def __init__(self):
		pass

class SVGgroup(SVGelement):
	def __init__(self, id):
		self.id = id
		self.children = []
	
	def add_children(self, children):
		self.children.append(children)

class SVGobject(SVGelement):
	def __init__(self, type, id):
		self.id = id
		self.type = type
