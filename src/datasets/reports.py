from xml.dom import minidom


class PathologyXMLReport:

    def __init__(self, fn):
        self.fn = fn
        self.sections = []
        dom = minidom.parse(self.fn)
        self.parse(dom)

    def __repr__(self):
        return f'PathologyXLMReport(fn={self.fn})'

    def __getitem__(self, index):
        text = '\n'.join(self.sections)
        return text[index]

    def parse(self, node):
        if node.hasAttribute('naaccrId'):
            self.sections.append(node.getAttribute('naaccrId'))

        # NOTE: nodeType is a Text node
        if node.nodeType == 3:
            self.sections.append(node.nodeValue)
        elif node.hasChildNodes():
            for child in node.childNodes:
                self.parse(child)
