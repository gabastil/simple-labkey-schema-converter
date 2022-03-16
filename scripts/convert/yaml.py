#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from src.converter import LabKeySchema
from optparse import OptionParser
import os

CONFIG = {
    "engine_version": "histologyMismatchAndAnnotation",
    "control_info": {
        "defaults": {
            "control_info": ["disease_group",
                             "doc_date",
                             "doc_name",
                             "doc_type",
                             "doc_version",
                             "engine_version",
                             "process_date",
                             "reference_id",
                             "source",
                             "metadata"]
        }
    }

}


def main(options):
    make_filenames(options)
    print(f"{f' YAML CONVERTER ':-^80}")
    print(f"Filename: {options.filename}\nOutput dir: {options.output_dir}")

    schema = LabKeySchema(options.filename, options=options)
    schema.save(options.output)


def make_filenames(options):
    options.filename = os.path.join(options.data_dir, options.file)
    output_filename = f"{os.path.basename(options.file).split('.')[0]}.json"
    options.output_filename = os.path.join(options.output_dir, output_filename)


if __name__ == "__main__":
    # parser = get_option_parser()
    parser = OptionParser("CLI tool to convert YAML schemas to JSON")
    parser.add_option("--file", "-f")
    parser.add_option("--data_dir", default="data/dataset/reports")
    parser.add_option("--output_dir", default="data/output/converted")
    parser.add_option("--disease_group", default="*")
    parser.add_option("--docDate", default=None)
    parser.add_option("--docName", default=None)
    parser.add_option("--docType", default="pathology")
    parser.add_option("--engine_version", default=CONFIG['engine_version'])
    parser.add_option("--process_date", default=None)
    parser.add_option("--reference_id", default=None)
    parser.add_option("--control_info_fields", default=CONFIG['control_info'])
    main(parser.parse_args()[0])
