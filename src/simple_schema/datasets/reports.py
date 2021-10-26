from xml.dom import minidom
import os

NAACCR = 'naaccrId'


class PathologyXMLReport:

    def __init__(self, fn, strip=False):
        self.fn = fn
        self._strip = strip
        self._sections = []
        self.parse(minidom.parse(self.fn))

    def __repr__(self):
        return f"PathologyXLMReport('{self.fn}')"

    def __getitem__(self, index):
        text = '\n'.join(self._sections)
        return text[index]

    def _append(self, text):
        if self._strip:
            text = text.strip()
        self._sections.append(text)

    def parse(self, node):
        if isinstance(node, list):
            for childNode in node:
                self.parse(childNode)
        elif node.nodeType == node.DOCUMENT_NODE:
            self.parse(node.childNodes)
        elif node.nodeType == node.TEXT_NODE:
            self._append(node.wholeText)
        elif node.nodeType == node.ELEMENT_NODE:
            self._append(node.getAttribute(NAACCR))
            self.parse(node.childNodes)

    def get_excerpts(self, indices):
        for start, stop in indices:
            yield self[start:stop]
