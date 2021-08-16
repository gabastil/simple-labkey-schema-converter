#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from src.converter import LabKeySchema
from optparse import OptionParser
from pathlib import Path
from box import Box
import os


def main(options):
    options.filename = Path(os.path.dirname(__file__),
                            options.source_dir,
                            options.filename)

    schema = LabKeySchema(options.filename, options=options)
    schema.save(options.output)


def load_configuration(fp='config.yml', basedir='config'):
    with open(os.path.join(basedir, fp)) as fin:
        return Box.from_yaml(fin)


def get_option_parser(fp='config.yml', basedir='config'):
    config_yml = load_configuration(fp, basedir)

    parser = OptionParser('CLI tool to generate new schemas')
    for option in config_yml.cli:
        parser.add_option(*option.flags, **option.kwargs)

    return parser


if __name__ == "__main__":
    parser = get_option_parser()
    options, *_ = parser.parse_args()

    print(f'Converting schema at {options.filename}')
    main(options)
