"""
This package allows for parsing of Cloverleaf log files into structured data.
The structured data can later be rendered for quick inspection, e.g. as a CSV table.

\author Pavlo Dyban (Doctolib GmbH)
\date   23-Jan-2020
"""

import argparse
import cloverleaf_parser
import json

def main():
    parser = argparse.ArgumentParser(description="Parse Cloverleaf logfiles into structured data representation.")
    parser.add_argument('file', help="path to the log file, e.g. test.log")
    parser.add_argument('outfile', help="path to the output JSON file, e.g. test.json")
    parser.add_argument('--encoding', help='encoding of the log file, e.g. latin1', type=str, default='utf-8')
    parser.add_argument('--mappingfile', help='JSON file containing field mapping', type=str)
    parser.add_argument('--filterfile', help='JSON file containing field filter (filter is applied after mapping)', type=str)

    args = parser.parse_args()

    cloverleaf_parser.verify_file(args.file)

    parser = cloverleaf_parser.parse(filename=args.file, encoding=args.encoding)

    if args.mappingfile:
        with open(args.mappingfile) as f:
            mapping = json.load(f)
        parser.map_fields(mapping)

    if args.filterfile:
        with open(args.filterfile) as f:
            filter = json.load(f)
        parser.filter_fields(filter)

    cloverleaf_parser.write_to_json(parser, out_file=args.outfile, encoding=args.encoding)


if __name__ == '__main__':
    main()
