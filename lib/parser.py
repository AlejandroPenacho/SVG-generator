from .svg_structs import *



class SVGfile:
    def __init__(self, filename):
        self.file = open(filename)
        self.buffer = ''

    def close(self):
        self.file.close()

    def get_next_element(self):
        self.find_block()
        type, block_text = self.read_block()

        if type == 'closure':
            return ('closure', None)
        
        if type == 'childless':
            return ('element', SVGsingle(*self.parse_block(block_text)))

        current_element = SVGgroup(*self.parse_block(block_text))

        while True:
            (element_type, next_child) = self.get_next_element()
            if element_type == 'closure':
                return ('element', current_element)
            elif element_type == 'element':
                current_element.children.append(next_child)

    def find_block(self):
        # This will traverse the file until it finds the start of a block (<)

        while True:
            splitted = self.buffer.split('<', 1)
            if len(splitted) == 2:
                self.buffer = splitted[1]
                return

            self.buffer = next(self.file)

    def read_block(self):
        text = ""
        while True:
            current_split = self.buffer.split(">", 1)
            if len(current_split) == 2:
                self.buffer = current_split[1]
                return self.classify_block(text+current_split[0])
            
            text += current_split[0]
            self.buffer = next(self.file)

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
       
