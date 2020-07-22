#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from converter import LabKeySchema
from optparse import OptionParser

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-f', '--filename', dest='filename', default='resources/schema.txt')

    (options, args) = parser.parse_args()

    schema = LabKeySchema(options.filename)
    print(schema.save())
