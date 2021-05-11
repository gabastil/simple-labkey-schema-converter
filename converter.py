#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from collections import OrderedDict
from pathlib import Path
import yaml
import json

class Schema:
    ''' Base class for Schema conversion. '''

    def __init__(self, path=None):
        ''' Assign path to YAML file to convert to JSON to path property '''
        self.path = Path(path) if path is not None else path

    def _path(self, path=None):
        ''' Return the correct path to use for the schema

        Args:
            path (str, optional): Path to return if present. Defaults to None.

        Returns:
            pathlib.Path: User input path as a Path object. None if none specified.
        '''
        return Path(path) if path is not None else self.path

    def load(self, path=None):
        ''' Retrun a dict from a yaml-structure schema file

        Args:
            path (str, optional): Path to yml file. Defaults to None.

        Raises:
            ValueError: Raised if no path specified in function or class

        Returns:
            dict: dictionary object with yaml file contents
        '''
        path = self._path(path)

        if path:
            with open(path) as data:
                return yaml.load(data, yaml.Loader)

        raise ValueError("Path to file to convert not defined")


class LabKeySchema(Schema):

    def __init__(self, path=None, indent=4):
        super().__init__(path)
        self.indent = indent

    def __repr__(self):
        ''' Pretty print the converted schema '''
        schema = self.convert()
        return json.dumps(schema, indent=self.indent)

    def convert(self):
        ''' Convert a yaml-like schema to LabKey's json format '''
        data = self.load()

        tables = []

        for table_name, fields in data.items():

            # TODO: Account for nested tables
            if isinstance(fields, dict):
                fields = self.parse(fields)

            table = OrderedDict(table=table_name, fields=fields)
            tables.append(table)

        groupings = [self._set_group("table"), self._set_group("field")]
        pathology = OrderedDict(groupings=groupings, tables=tables)
        return OrderedDict(pathology=pathology)

    def parse(self, fields):
        ''' Return a list of field values converted to LabKey's format '''
        parsed = []

        if fields:
            for field, values in fields.items():
                if len(values) == 0:
                    values = [""]
                field_ = self._set_field(field, values)
                parsed.append(field_)

        return parsed

    def _set_data(self, type_='string'):
        ''' Return the correct data type based on user input.

        Args:
            type_ (str): date, string, number. Default is 'string'.

        Returns:
            string: Assigned data type per LabKey schema specifications.

        Reference:
            https://www.labkey.org/Documentation/wiki-page.view?name=metadataJson
        '''
        if type_.lower() == 'date':
            return 'date'
        return 'string'

    def _set_class(self, class_):
        ''' Return boolean for correct class type based on user input.

        Args:
            class_ (str): Closed or open class

        Returns:
            bool: True if closed class, False if open class per LabKey schema
            specifications.

        Reference:
            https://www.labkey.org/Documentation/wiki-page.view?name=metadataJson
        '''
        if class_.lower().startswith('c'):
            return True
        return False

    def _set_selection(self, selection):
        ''' Return a boolean for correct selection type based on user input.

        Args:
            selection (str): Single or multiple

        Returns:
            bool: True if multiValue indicated, False if single.

        Reference:
            https://www.labkey.org/Documentation/wiki-page.view?name=metadataJson
        '''
        return selection.lower().startswith('mu')

    def _set_field(self, name, values):
        ''' Create a Field object (dict) for insertion into the schema.

        Parameters
        ----------
            name (str): field name
            values (list): Class, datatype, multiValue, and field values
        '''
        field = OrderedDict(field=name)

        class_, selection_, type_, *values_ = values

        if isinstance(class_, dict):
            class_, fields_listened_, triggers_ = class_['Linked']

            # How to handle the conditional field
            handlers = OrderedDict(values=triggers_, success='SHOW', failure='HIDE')
            listeners = OrderedDict(field=fields_listened_, handlers=[handlers])
            field['listeners'] = [listeners]
            field['hidden'] = True

        field['datatype'] = self._set_data(type_)
        field['closedClass'] = self._set_class(class_)
        field['multiValue'] = self._set_selection(selection_)
        field['diseaseProperties'] = [OrderedDict(diseaseGroup=['*'], values=values_)]

        return field

    def _set_group(self, level, order="alpha", orientation="horizontal"):
        return OrderedDict(level=level, order=order, orientation=orientation)

    def save(self, path=None):
        ''' Convert and save a yaml-like schema to LabKey's format '''
        path = self._path(path)
        save_path = path.parent / f'{path.stem}.json'

        with open(save_path, 'w') as pout:
            json.dump(self.convert(), pout, indent=self.indent)
