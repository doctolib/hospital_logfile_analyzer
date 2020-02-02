"""
The implementation of the Cloverleaf logfile parser.
"""
import os.path
import json
from .logfile_parser import LogfileParser


class CloverleafLogfileParser(LogfileParser):
    """
    The Cloverleaf logfile parser implementation.

    For an example of a Cloverleaf logfile, see logfiles in test folder.
    """
    def parse(self, iterable):
        for line in iterable:
            self.append(line)

    def append(self, line):
        if not line.strip():
            # skip empty lines
            return

        if 'com.infor.cloverleaf' in line:
            event = {}
            event['time'] = ' '.join(line.split(' ')[:5])
            event['handle'] = 'com.infor.cloverleaf.gjdws.handlers.RawHandler'
            self.events.append(event)

        elif 'INFO: ' in line:
            event = self.events[-1]
            event['direction'] = line[6:].replace(':', '').strip()
            event['info'] = {}
            self.current_event_child = event['info']

        elif '----------------' in line:
            event = self.events[-1]
            event_name = line.replace('-', '').strip()
            event[event_name] = {}
            self.current_event_child = event[event_name]

        elif '=' in line:
            # append key, value dictionary to the currently active child
            child = self.current_event_child
            key, value = line.split('=', 1)
            child[key.strip()] = value.strip()

        elif 'Response Code:' in line:
            child = self.current_event_child
            key, value = line.split(':', 1)
            child[key.strip()] = value.strip()

        elif 'Engine idle' in line:
            pass

        else:
            # non-empty line, free format should be appended as key, value
            child = self.current_event_child
            child['text'] = line.strip()

    def map_fields(self, mapping, copy=True):
        for src, dst in mapping.items():
            dst = dst.split('.')
            src = src.split('.')
            for event in self.events:
                try:
                    item_dst = event
                    item_src = event
                    for d in dst[:-1]:
                        item_dst = item_dst[d]
                    for s in src[:-1]:
                        item_src = item_src[s]
                        item_dst[dst[-1]] = item_src[src[-1]]
                    if not copy:
                        del item_src[src[-1]]

                except KeyError:
                    pass

    def filter_fields(self, filter):
        for event in self.events:
            for field_name, field_keep in filter.items():
                if not field_keep and field_name in event:
                    del event[field_name]


def parse(filename, encoding='utf8'):
    """
    Parses a multi-line text log file.

    @param filename Path to logfile for parsing.
    @param encoding The encoding of the logfile, default: UTF-8.
    @return Returns the parser.

    Currently only Cloverleaf logfiles are supported.
    """
    parser = CloverleafLogfileParser()
    with open(filename, encoding=encoding) as f:
        parser.parse(f)
    return parser


def verify_file(filename):
    """
    Verifies that a file exists.

    @param filename Path to file for verification.
    @return True if the file exists; false, otherwise.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError('{} cannot be found. Check the path to your file.'.format(filename))


def write_to_json(parser, out_file, encoding='utf8'):
    """
    Convenience function that writes the structured data representation to a JSON file.

    @param parser   Parser whose contents have to be serialized to JSON.
    @param out_file Path to file where the parser will be serialized to.
    @param encoding The encoding of the target file, default: UTF-8.
    """
    js = parser.events
    with open(out_file, 'w', encoding=encoding) as f_out:
        json.dump(js, f_out)
