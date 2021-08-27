
class SVGelement:
    # Base class for any possible element that may appear in an SVG file, 
    # including groups, single elements or text.

    def __init__(self, svg_type):
        self.svg_type = svg_type

    def __str__(self):
        return "Generic write of an SVG element"

    def __repr__(self):
        return "Quick representation of the element for debugging purposes"


class SVGgroup(SVGelement):
    # An SVG element that has children

    def __init__(self, name, data):
        super().__init__("group")
        self.name = name
        self.data = data
        self.children = []

    def __str__(self):
        text = f'<{self.name} ({len(self.data)} param) ({len(self.children)} children) />'
        return text

    def __repr__(self):
        return f'<{self.name} ({len(self.data)}/{len(self.children)}) />'

    def print_to_file(self, svg_file, ident=''):

        new_ident = ident + svg_file.ident_type
        text = f'{ident}<{self.name}'
        for param in self.data.keys():
            text += f'\n{new_ident}{param}="{self.data[param]}"'
        text += '>'

        if self.name != 'tspan' and self.name != 'text':
            text += '\n'

        svg_file.file.write(text)

        for child in self.children:
            child.print_to_file(svg_file, new_ident)
        
        if self.name != 'tspan' and self.name != 'text':
            svg_file.file.write(f'{ident}</{self.name}>')
        else:
            svg_file.file.write(f'</{self.name}>')

        if self.name != "tspan":
            svg_file.file.write('\n')
        

class SVGsingle(SVGelement):
    def __init__(self, name, data):
        super().__init__("single")
        self.name = name
        self.data = data

    def __str__(self):
        text = f'<{self.name} ({len(self.data)} param) />'
        return text

    def __repr__(self):
        return f'<{self.name} ({len(self.data)}) />'
    
    def print_to_file(self, svg_file, ident=''):

        new_ident = ident + svg_file.ident_type
        text = f'{ident}<{self.name}'
        for param in self.data.keys():
            text += f'\n{new_ident}{param}="{self.data[param]}"'
        text += '/>\n'
        svg_file.file.write(text)


class SVGtext(SVGelement):
    def __init__(self, text):
        super().__init__("text")
        self.text = text

    def __str__(self):
        text = f'<text />'
        return text

    def __repr__(self):
        return f'<text />'

    def print_to_file(self, svg_file, ident=''):
        svg_file.file.write(self.text)
