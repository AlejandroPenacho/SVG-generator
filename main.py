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


def addElement(filename):
	# Gets the data and children of the next element in the file. Since the next
	# line can contain the end of the current element (like </circle>), the
	# output value has two elements : [endCurrentElement, element]. 

	[type, element] = getElementData(filename)	
	if (type == "endCurrentElement"):
		return [True, 0]
	else if (type == "noChildren"):
		return [False, element]
	
	while True:
		[type, element] = addElement(filename)	
		if (type == "endCurrentElement"):
			return [False, element]
		else:
			element.addChildren(element)
		
	

def getElementData(filename):
	# Reads all information between two traingular brackets (<>). These contain
	# an end of element, or the information regarding a new one. Depending on
	# whether it ends with ">" or "/>", the next elements will be children of
	# this one. Therefore, the ouput of the function consists on two values:
	# [type, element]. Type can be: "endElement", "noChildren" or "withChildren".
	#
	#	- "endCurrentElement": single line indicating the exit of the current element,
	#	  					   </***>.
	#	- "noChilden": an element with no children, so it can be added
	#				   inmediately to the children of the parent element.
	#	- "withChidlren": element with children, so elements must be added to it
	#					  as children until an "endCurrentElement" is read.

