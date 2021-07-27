# import pdb
# pdb.set_trace()
import copy

def flatten(list):
	# Takes a list of lists and return a single list, by concatenating 
	# the elements
	return [x for xx in list for x in xx]


class SVGelement:
	# Represents a single SVG element, whether a single object, a group,
	# or the root element (<svg>)

	def __init__(self):
		# Creates the basic element, with no data attached to it

		self.type = ""
		self.data = {}
		self.children = []
		self.parent = None
		self.depth = 0

	def add_children(self, children):
		self.children.append(children)

	def __str__(self):
		out = f"<{self.type}"
		for key,val in self.data.items():
			out += f"\n\t{key}\t:\t{val}"
		out+= "\t>\n"
		if len(self.children)>0:
			out += f"\nWith {len(self.children)} children\n"
		return out

	def __repr__(self):
		out = f"<{self.type}/>"
		if len(self.children)>0:
			out += f" +{len(self.children)}"
		return out

	def print_to_file(self, file, left_tabs=0):
		
		pre_space = "\t" * left_tabs
		file.write(f"{pre_space}<{self.type}")

		for key,val in self.data.items():
			file.write(f"\n{pre_space}\t{key}=\"{val}\"")

		if len(self.children)==0:
			file.write("/>\n")
			return
		
		file.write(">\n")
		for child in self.children:
			child.print_to_file(file, left_tabs+1)
		file.write(f"{pre_space}</{self.type}>\n")

	
	def modify(self, pre_fun=(lambda x: [x]), pos_fun=(lambda x: [x])):

		# Function to modify SVG elements recursively. It performs the pre_fun
		# on the element, then the whole modification on each children, and
		# then the pos_fun. It is able to handle modifications that involve
		# generating more elements, or deleting them.
		#
		# The pre_fun and the pos_fun must be functions that take a SVGelement,
		# and return a list of SVGelements. The modify method takes care of
		# flattening the list. It is recommended to use deepcopy in the
		# functions, since the default behaviour of python just uses references,
		# and can lead to the same element being modified several times.

		list_of_pre_elements = pre_fun(self)

		for pre_element in list_of_pre_elements:
			new_children = []
			for child in pre_element.children:
				new_children.append(child.modify(pre_fun, pos_fun))
			pre_element.children = flatten(new_children)
		

		element_flat_list = flatten(map(pos_fun, list_of_pre_elements))

		if (self.depth == 0):
			return element_flat_list[0]
		else:
			return element_flat_list


def parse_svg(filename, skip_lines=2):
	# Takes an SVG file by name, and returns its root element
	
	file = open(filename)
	[file.readline() for i in range(skip_lines)]
	return add_element(file)[1]

def add_element(file, depth=0, parent = None):
	# Gets the data and children of the next element in the file. Since the next
	# line can contain the end of the current element (like </circle>), the
	# output value has two elements : [endCurrentElement, element]. 

	[type, element] = get_block(file)	
	if (type == "endCurrentElement"):
		return [True, 0]

	element.parent = parent
	element.depth = depth

	if (type == "noChildren"):
		return [False, element]

	else:
		while True:
			[endThisElement, child] = add_element(file, depth=(depth+1), parent=element)
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
	# Takes of block of data (starting with < and ending with >) and creates
	# an SVG element out of it. The depth, parent and children of the element
	# must be obtained later

	new_element = SVGelement()

	for index, line in enumerate(data_lines):
		processed_line = line.lstrip("<").rstrip(" />").split("=", 1)
		if index == 0:
			new_element.type = processed_line[0]
		else:
			new_element.data.update({processed_line[0]: processed_line[1].strip('"')})

	return new_element
