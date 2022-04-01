from xml.dom import minidom
import os

NAACCR = 'naaccrId'


class PathologyXMLReport:

    def __init__(self, fn, strip=False, offset=0):
        self.fn = fn
        self._strip = strip
        self.offset = offset
        self._sections = []
        self.parse(minidom.parse(self.fn))
        if strip:
            self._sections = list(filter(len, self._sections))

    def __repr__(self):
        return f"PathologyXLMReport('{self.fn}')"

    def __getitem__(self, index):
        text = ''.join(filter(len, self.sections))
        return text[index]

    @property
    def sections(self):
        return self._sections

    @property
    def strip(self):
        return self._strip

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, offset):
        self._offset = int(offset)

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
            start -= self.offset
            stop -= self.offset
            yield self[start:stop]
