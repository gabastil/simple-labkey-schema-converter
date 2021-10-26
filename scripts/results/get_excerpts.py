from src import PathologyXMLReport
from argparse import ArgumentParser
import pandas as pd
import os


def main(args):
    results_file = open_results_file(args)
    source_file = open_source_file(args)
    excerpt = source_file.get_excerpts(results_file.values)
    results_file = results_file.assign(excerpt=excerpt)
    save(results_file, args)


def open_results_file(args):
    fp = os.path.join(args.results_dir, args.results_file)
    return pd.read_csv(fp)


def open_source_file(args):
    fp = os.path.join(args.source_dir, args.source_file)
    return PathologyXMLReport(fp)


def save(dataframe, args):
    fp = os.path.join(args.output_dir, f'{args.results_file}-excerpts.csv')
    dataframe.to_csv(fp, index=False)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--results_file',
                        help='Results data with indices to extract from --source_file.')
    parser.add_argument('--source_file',
                        help='Document with text to extract results from.')
    parser.add_argument('--results_dir', default='data/dataset/results')
    parser.add_argument('--source_dir', default='data/dataset/reports')
    parser.add_argument('--output_dir', default='data/output/scripts/results')
    parser.add_argument()
    main(parser.parse_args())
