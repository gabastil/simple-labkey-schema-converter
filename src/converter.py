from collections import OrderedDict
from pathlib import Path
from typing import List
import yaml
import json


class Schema:
    """ Base class for Schema conversion. """

    def __init__(self, path: str = None):
        self.path = Path(path) if path is not None else path

    def _path(self, path: str = None) -> Path:
        return Path(path) if path is not None else self.path

    def load(self, path: str = None) -> dict:
        path = self._path(path)

        if path:
            with open(path) as data:
                return yaml.load(data, yaml.Loader)

        raise ValueError(f'"{path}" not a valid filepath.')


class LabKeySchema(Schema):
    """ YAML to JSON schema converter for LabKey annotation. The JSON schema is
    based on the LabKey documentation online at
    - https://www.labkey.org/Documentation/wiki-page.view?name=metadataJson
    """

    def __init__(self, path: str = None, indent: int = 4, options: dict = None):
        super().__init__(path)
        self.indent = indent
        self.options = options

    def __repr__(self):
        schema = self.convert()
        return json.dumps(schema, indent=self.indent)

    def convert(self) -> OrderedDict:
        data = self.load()
        tables = []
        for table_name, fields in data.items():

            # TODO: Account for nested tables
            if isinstance(fields, dict):
                fields = self.parse(fields)

            table = OrderedDict(table=table_name, fields=fields)
            tables.append(table)

        groupings = [
            self._set_group("table"),
            self._set_group("field"),
            self._set_group("recordKey")  # NOTE: Enable nested specimen tables
        ]

        pathology = OrderedDict(groupings=groupings, tables=tables)
        return OrderedDict(pathology=pathology)

    def parse(self, fields: dict) -> List[OrderedDict]:
        """ Return a list of field values converted to LabKey's format """
        parsed = []

        if fields:
            for field, values in fields.items():
                if len(values) == 0:
                    values = [""]
                field_ = self._set_field(field, values)
                parsed.append(field_)

        return parsed

    def _set_field(self, name: str, values: List[str]) -> OrderedDict:
        """ Create a Field object (dict) for insertion into the schema. """
        field = OrderedDict(field=name)
        class_, selection_, type_, *values_ = values

        if isinstance(class_, dict):
            key = "Linked"
            if "linked" in class_:
                key = key.lower()
            class_, fields_listened_, triggers_ = class_[key]

            # NOTE: Conditional field handling
            handlers = OrderedDict(
                values=triggers_,
                success="SHOW",
                failure="HIDE"
            )
            listeners = OrderedDict(
                field=fields_listened_,
                handlers=[handlers]
            )
            field["listeners"] = [listeners]
            field["hidden"] = True

        field["datatype"] = self._set_data(type_)
        field["closedClass"] = self._set_class(class_)
        field["multiValue"] = self._set_selection(selection_)
        field["diseaseProperties"] = [
            OrderedDict(diseaseGroup=['*'], values=values_)
        ]

        return field

    def _set_data(self, dtype: str = "string") -> str:
        """ Return the correct data type based on user input. """
        if dtype.lower().startswith("date"):
            return "date"
        return "string"

    def _set_class(self, class_: str) -> bool:
        """ Return boolean for correct class type based on user input. """
        return class_.lower().startswith("close")

    def _set_selection(self, selection: str) -> bool:
        """ Return a boolean for correct selection type based on input. """
        return selection.lower().startswith("multiple")

    def _set_group(self,
                   level: str,
                   order: str = "alpha",
                   orientation: str = "horizontal") -> OrderedDict:
        return OrderedDict(level=level, order=order, orientation=orientation)

    def save(self, path: str = None):
        """ Convert and save a yaml-like schema to LabKey's format """
        path = self._path(path)
        with open(path.parent / f"{path.stem}.json", "w") as pout:
            json.dump(self.convert(), pout, indent=self.indent)
