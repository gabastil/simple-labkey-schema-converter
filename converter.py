#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from collections import OrderedDict
from pathlib import Path
import yaml
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)

class Schema:

    def __init__(self, path=None):
        self.path = Path(path) if path is not None else path

    def _path(self, path=None):
        return self.path if path is None else Path(path)

    def load(self, path=None):
        ''' Return a dict from a yaml-structured schema file '''
        path = self._path(path)

        if path:
            with open(path) as data:
                return yaml.load(data, yaml.Loader)

        raise ValueError("Path to file to convert to schema not defined")

class LabKeySchema(Schema):

    def __init__(self, path=None):
        super().__init__(path)

    def convert(self):
        ''' Convert a yaml-like schema to LabKey's json format '''
        data = self.load()

        tables = []

        for table_, fields_ in data.items():
            fields = self.parse(fields_)
            table = {"table" : table_, "fields" : fields}
            tables.append(table)

        groupings = [self._set_group("table"), self._set_group("field")]
        return {"pathology": {"groupings": groupings, "tables": tables}}

    def parse(self, fields):
        ''' Return a list of field values converted to LabKey's format '''
        parsed = []

        for field, values in fields.items():
            field_ = self._set_field(field, values)
            # pp.pprint(field_)
            parsed.append(field_)

        return parsed

    def _set_field(self, name, values):
        class_, type_, *values_ = values
        return {'field' : name,
                'datatype' : 'date' if type_.lower() == 'date' else 'string',
                'closedClass' : True if class_.lower().startswith('c') else False,
                'multiValue': False,
                'diseaseProperties' : [
                     {
                         'diseaseGroup': ["*"],
                         'values': values_
                     }
               ]}

    def _set_group(self, level, order="alpha", orientation="horizontal"):
        return dict(level=level, order=order, orientation=orientation)

    def save(self, path=None):
        ''' Convert and save a yaml-like schema to LabKey's format '''
        path = self._path(path)
        save_path = path.parent / f'{path.stem}.json'

        with open(save_path, 'w') as pout:
            json.dump(self.convert(), pout)


if __name__=="__main__":
    print(LabKeySchema('resources/schema.txt').save())
    # a, b, *c = Schema('resources/schema.txt').load()['Circumferential Resection Margin (CRM)']['Measurement Unit']
    # print(a, b, c)