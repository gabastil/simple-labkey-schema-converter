#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from collections import OrderedDict
import yaml
import json

SEP = ' ' * 4

def read_txt(filepath):
    ''' Read in the plain text schema text file and chunk

    Parameters
    ----------
        filepath (str): path to plain text file

    Returns
    -------
        List of schema components
    '''
    def prev(lines, index):
        try:
            return lines[index - 1]
        except IndexError:
            return None

    def post(lines, index):
        try:
            return lines[index + 1]
        except IndexError:
            return None

    def surroundings(lines, index):
        return prev(lines, index), post(lines, index)

    schema = OrderedDict()

    with open(path) as fin:
        lines = fin.readlines()

        h = 0
        for i, line in enumerate(lines):
            if indents(line) == 0 and i > 0:
                header, content = parse(lines, h, i)
                schema[header] = content
                h = i + 1

def indents(line):
    return line.count(SEP)

def parse(lines, start, finish, level=0):
    ''' Read a line and determine its schema role

    Parameters
    ----------
        lines (list): lines from plain text file
        start (int): first index
        finish (int): second index
    '''
    if not isinstance(lines, list):
        return lines

    level = lines[0].replace(SEP, '')

    if level == 0:
        content = parse(lines[1:], start, finish, level + 1)
    elif level >= 1:
        content =


    return {level : content}

    section, field, values = [[]] * 3
    h = 0

    for i, line in enumerate(lines[start:finish]):
        if indents(line) == 0:

def make_schema(filepath):
    ''' Return a schema for upload into LabKey

    Parameters
    ----------
        filepath (str): path to plain text file
    '''
    raw = read_txt(filepath)

if __name__ == "__main__":
    parse(['    section name',
           '        field',
           '        class',
           '        type',
           '        values',
           '        values',
           '            secondary values',
           ], 0, 7)