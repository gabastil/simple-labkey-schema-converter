#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import yaml
import json

def read_txt(path):
    ''' Read in the plain text schema text file and chunk

    Parameters
    ----------
        path (str): path to plain text file
    
    Returns
    -------
        List of schema components
    '''
    with open(path) as fin:
        raw = fin.readlines()
        raise NotImplementedError()

def parse(line, sep=" " * 4):
    ''' Read a line and determine its schema role

    Parameters
    ----------
        line (str): line from plain text file
        sep (str): spacing indicator for role
    '''
    pass

def make_schema():
    ''' Return a schema for upload into LabKey
    '''
    pass
