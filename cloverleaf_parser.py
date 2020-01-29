"""
The implementation of the Cloverleaf logfile parser.
"""
import os.path
import json


class CloverleafParser:
    """
    The Cloverleaf logfile implementation.
    """
    def __init__(self):
        self.events = []
        self.current_event_child = None

    def parse(self, iterable):
        """
        Main function which parses a multi-line text log file.

        \param iterable An iterable object that represents a multi-line log
                        file, e.g. a File object or a list of strings.
        """
        for line in iterable:
            self.append(line)

    def append(self, line):
        """
        Append next line from a multiline file.
        """
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
        """
        Transforms fields using the mapping rules.

        \param mapping  Dictionary containing source, destination key-value pairs.
                        Multi-level paths should be dot-separated, e.g.
                        {"Response information.Response Code": "Response Code"}
                        will assign the value stored in
                        data[Response information][Response Code] to
                        data[Response Code].
        \param copy     If true, will keep the mapped value both in the source
                        and target location. If false, will move the value from
                        source to target.
        """
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
        """
        Removes fields that are marked as false in filter.

        \param filter   Dictionary that contains key-value pairs.
                        If a value is set to False for a given field, this
                        field will be filtered for every event where present.
        """
        for event in self.events:
            for field_name, field_keep in filter.items():
                if not field_keep and field_name in event:
                    del event[field_name]

def parse(filename, encoding='utf8'):
    """
    Parses a multi-line text log file.
    """
    parser = CloverleafParser()
    with open(filename, encoding=encoding) as f:
        parser.parse(f)
    return parser

def verify_file(filename):
    """
    Verifies that a file exists.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError('{} cannot be found. Check the path to your file.'.format(filename))

def write_to_json(parser, out_file, encoding='utf8'):
    """
    Convenience function that writes the structured data representation to a JSON file.
    """
    js = parser.events
    with open(out_file, 'w', encoding=encoding) as f_out:
        json.dump(js, f_out)
