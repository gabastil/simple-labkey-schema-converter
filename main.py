#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from converter import make_schema
from sys import argv
from optparse import OptionParser

if __name__ == "__main__":
    optparser = OptionParser()

    filepath = "resources/template.txt"

    make_schema(filepath)
