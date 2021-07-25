# import pdb
# pdb.set_trace()

class SVGelement:
	def __init__(self):
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
			file.write(f"\n{pre_space}\t{key}={val}")

		if len(self.children)==0:
			file.write("/>\n")
			return
		
		file.write(">\n")
		for child in self.children:
			child.print_to_file(file, left_tabs+1)
		file.write(f"{pre_space}</{self.type}>\n")


def parse_svg(filename, skip_lines=2):
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

	new_element = SVGelement()

	for index, line in enumerate(data_lines):
		processed_line = line.lstrip("<").rstrip(" />").split("=", 1)
		if index == 0:
			new_element.type = processed_line[0]
		else:
			new_element.data.update({processed_line[0]: processed_line[1]})

	return new_element

out = parse_svg("test/baseDice.svg", 3)
newf = open("test/out.svg","w")
out.print_to_file(newf)
newf.close()
