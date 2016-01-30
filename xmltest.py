import xml.etree.ElementTree as etree

class Object():
    def __init__(self, args, parent, text):
        self.children = []
        self.args = args
        self.parent = parent
        self.text = text
    def add_child(self, child):
        self.children.append(child)
    def str(self):
        print("Object:", self.args, "Parent:", self.parent, "Children:", self.children, "Text:", self.text)
        if len(self.children) > 0:
            for child in self.children:
                child.str()
class Div():
    def __init__(self, args, parent, text):
        self.children = []
        self.args = args
        self.parent = parent
        self.text = text
    def add_child(self, child):
        self.children.append(child)
    def str(self):
        print("Div:", self.args, "Parent:", self.parent, "Children:", self.children, "Text:", self.text)
        if len(self.children) > 0:
            for child in self.children:
                child.str()

classes = {"object": Object, "div": Div}

class Main():
    def __init__(self):
        self.children = []
    def add_child(self, child):
        self.children.append(child)
    def load_xml(self, file):
        self.root = etree.parse(file).getroot()
        self.convert(self.root, self)
    def convert(self, root, parent):
        for child in root:
            conv_object = classes[child.tag](child.attrib, parent, child.text)
            parent.add_child(conv_object)
            if len(child) > 0:
                self.convert(child, conv_object)
    def str(self):
        print("Main:", "Children:", self.children)
        if len(self.children) > 0:
            for child in self.children:
                child.str()
main = Main()
main.load_xml("xmltest.xml")
main.str()