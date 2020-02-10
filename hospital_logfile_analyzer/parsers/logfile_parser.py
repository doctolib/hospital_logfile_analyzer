"""
The interface for logfile parsers.
"""

class LogfileParser:
    def __init__(self):
        self.events = []
        self.current_event_child = None

    def parse(self, iterable):
        """
        Main function which parses a multi-line text log file and creates
        a structured data representation of the file's contents.

        @param iterable An iterable object that represents a multi-line log
                        file, e.g. a File object or a list of strings.
        """
        raise NotImplementedError('An abstract parent class cannot be instatiated directly.')

    def append(self, line):
        """
        Append next line from a multiline file.

        @param line The text line that will be processed by the parser and appended to the structured data.
        """
        raise NotImplementedError('An abstract parent class cannot be instatiated directly.')

    def filter_fields(self, filter):
        """
        Removes fields that are marked as false in filter.

        @param filter   Dictionary that contains key-value pairs.
                        If a value is set to False for a given field, this
                        field will be filtered out for every event where present.
        """
        raise NotImplementedError('An abstract parent class cannot be instatiated directly.')

    def map_fields(self, mapping, copy=True):
        """
        Transforms fields using the mapping rules.

        @param mapping  Dictionary containing source, destination key-value pairs.
                        Multi-level paths should be dot-separated, e.g.
                        {"Response information.Response Code": "Response Code"}
                        will assign the value stored in
                        data[Response information][Response Code] to
                        data[Response Code].
        @param copy     If true, will keep the mapped value both in the source
                        and target location. If false, will move the value from
                        source to target. Default: True.
        """
        raise NotImplementedError('An abstract parent class cannot be instatiated directly.')
