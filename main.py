#import pdb
#pdb.set_trace()

class SVGelement:
	def __init__(self, id):
		self.id = id
		self.children = []

	def add_children(self, children):
		self.children.append(children)


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


def parse_svg(filename):
	file = open(filename)
	return add_element(file)

def add_element(file):
	# Gets the data and children of the next element in the file. Since the next
	# line can contain the end of the current element (like </circle>), the
	# output value has two elements : [endCurrentElement, element]. 

	[type, element] = get_block(file)	
	if (type == "endCurrentElement"):
		return [True, 0]
	elif (type == "noChildren"):
		return [False, element]
	
	while True:
		[endThisElement, child] = add_element(file)	
		if endThisElement:
			return [False, element]
		else:
			element.add_children(child)
		
	

def get_block(file):
	# Reads all information between two traingular brackets (<>). These contain
	# an end of element, or the information regarding a new one. Depending on
	# whether it ends with ">" or "/>", the next elements will be children of
	# this one. Therefore, the ouput of the function consists on two values:
	# [type, element]. Type can be: "endElement", "noChildren" or "withChildren".
	#
	#	- "endCurrentElement": single line indicating the exit of the current element,
	#		   </***>.
	#	- "noChilden": an element with no children, so it can be added
	#	   inmediately to the children of the parent element.
	#	- "withChidlren": element with children, so elements must be added to it
	#		  as children until an "endCurrentElement" is read.

	data_lines = [file.readline().strip()]
	if (data_lines[0][0:2] == "</"):
		return ["endCurrentElement", 0]

	while True:
		if data_lines[-1][-1] == ">":
			break
		else:
			data_lines.append(file.readline().strip())

	if data_lines[-1][-2:] == "/>":
		childrenStatus = "noChildren"
	else:
		childrenStatus = "withChildren"

	return [childrenStatus, process_block(data_lines)]


def process_block(data_lines):
	out = SVGelement("www")
	out.data = data_lines
	return out

out = parse_svg("test/example.svg")

