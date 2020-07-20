#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import yaml
import json

def read_txt(filepath, sept=' '*4):
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

    def indents(line):
        return line.count(sep)

    schema, section, values = [], [], []

    with open(path) as fin:
        lines = fin.readlines()

        for i, line in enumerate(lines):
            before, after = surroundings(lines, i)

            if before is not None:
                if indents(line) > indents(before):

                
def parse(line, sep):
    ''' Read a line and determine its schema role

    Parameters
    ----------
        line (str): line from plain text file
        sep (str): spacing indicator for role
    '''
    pass

def make_schema(filepath):
    ''' Return a schema for upload into LabKey

    Parameters
    ----------
        filepath (str): path to plain text file
    '''
    raw = read_txt(filepath)
