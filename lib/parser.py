from .svg_structs import *



class SVGfile:
    def __init__(self, filename, mode='r'):
        self.file = open(filename, mode)
        self.buffer = ''
        self.ident_type = '   '

    def close(self):
        self.file.close()

    def get_next_element(self):
        self.find_block()
        element_type, block_text = self.read_block()

        if element_type == 'closure':
            return ('closure', None)
        
        if element_type == 'childless':
            return ('element', SVGsingle(*self.parse_block(block_text)))

        current_element = SVGgroup(*self.parse_block(block_text))

        if current_element.name == "text":
            return self.get_text_group_children(current_element)
        else:
            return self.get_normal_group_children(current_element)


    def get_next_text_element(self):
        first_char = self.read_next()
        if first_char == '<':
            element_type, block_text = self.read_block()
            if element_type=="closure":
                return ('closure', None)
            else:
                current_element = SVGgroup(*self.parse_block(block_text))
                return self.get_text_group_children(current_element)
            
        else:
            full_text = first_char + self.read_until('<')
            self.buffer = '<' + self.buffer
            return ('element', SVGtext(full_text))



    def get_normal_group_children(self, parent):
        while True:
            (element_type, next_child) = self.get_next_element()
            if element_type == 'closure':
                return ('element', parent)
            elif element_type == 'element':
                parent.children.append(next_child)


    def get_text_group_children(self, parent):
        while True:
            (element_type, next_child) = self.get_next_text_element()
            if element_type == 'closure':
                return ('element', parent)
            elif element_type == 'element':
                parent.children.append(next_child)



    def find_block(self):
        # This will traverse the file until it finds the start of a block (<)
        self.read_until('<')

    def read_block(self):
        return self.classify_block(self.read_until('>'))


    def classify_block(self, text):
        if text[0] == '/':
            return ("closure", text[1:])
        elif text[-1] == '/':
            return ("childless", text[:-1])
        else:
            return ("childfull", text)


    def parse_svg(self, skip_lines):
        [next(self.file) for i in range(skip_lines)]
        return self.get_next_element()[1]

    def parse_block(self, text_block):
        [name, data_text] = text_block.split(None, 1)

        data = {}
        while True:
            data_text = data_text.lstrip()
            if data_text == '':
                break
            [param_name, data_text] = data_text.split('=',1)
            [_,param_val, data_text] = data_text.split('"', 2)
            data.update({param_name: param_val})

        return [name, data]
            
    def read_until(self, limit_char):
        text = ''
        while True:
            splitted = self.buffer.split(limit_char, 1)
            text += splitted[0]
            if len(splitted) == 2:
                self.buffer = splitted[1]
                return text

            self.buffer = next(self.file)

    def read_next(self):
        if self.buffer == '':
            self.buffer = next(self.file)

        char = self.buffer[0]
        self.buffer = self.buffer[1:]
        return char