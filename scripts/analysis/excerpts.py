from argparse import ArgumentParser
from xml.dom import minidom
import pandas as pd
import os


def main(opts):
    print(f'{f" EXCERPTS.PY ":=^80}')
    results, source = load_files(opts)
    indices = get_indices(results, opts)
    results = results.append(excerpt=get_excerpts(source, indices, opts))
    results.to_csv(os.path.join(opts.output_dir, opts.results_file))
    print(f'{f" COMPLETED ":=^80}')


def load_files(opts):
    results = os.path.join(opts.data_dir, opts.results_file)
    source = os.path.join(opts.data_dir, opts.source_file)
    return pd.read_excel(results), minidom.parse(source)


def get_indices(results, opts):
    return results[['Start', 'Stop']]


def get_excerpts(source, indices, opts):
    source_text = None
    excerpts = []
    for i, (start, stop) in indices.iterrows():
        excerpts.append(source_text[start:stop])
    return excerpts


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '--results_file',
        help='Data from LabKey with Start, Stop indices')
    parser.add_argument(
        '--source_file',
        help='Pathology report XML file name.')
    parser.add_argument(
        '--data_dir',
        default='data/dataset',
        help='Path to data folder with resuls and source files')
    parser.add_argument(
        '--output_dir',
        default='data/output',
        help='Path to output results with excerpts.')
    main(parser.parse_args())
