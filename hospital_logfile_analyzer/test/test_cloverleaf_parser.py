"""
Test suite for CloverleafParser
"""
import unittest
from hospital_logfile_analyzer.parsers import CloverleafLogfileParser
import json


class TestCloverleafParser(unittest.TestCase):
    def setUp(self):
        self.parser = CloverleafLogfileParser()
        self.example_logfile = "hospital_logfile_analyzer/test/test.log"
        with open(self.example_logfile) as f:
            self.parser.parse(f)

    def tearDown(self):
        pass

    def test_initialization(self):
        self.assertEqual(len(self.parser.events), 6)

    def test_can_parse_example_file(self):
        self.assertEqual(len(self.parser.events), 6)
        with open("hospital_logfile_analyzer/test/test_cloverleaf_parser_expected_results.json") as f:
            expected_events = json.load(f)
            for event_index, expected_event in enumerate(expected_events):
                event = self.parser.events[event_index]
                for key, expected_value in expected_event.items():
                    self.assertEqual(event[key], expected_value)

    def test_mapping(self):
        mapping = {'Response information.Response Code': 'Response Code'}
        self.parser.map_fields(mapping)
        expected_events = (1,)
        for event_index in expected_events:
            self.assertIn('Response Code', self.parser.events[event_index])

    def test_filters(self):
        filter = {'Headers': False}
        self.parser.filter_fields(filter)
        expected_events = (1,)
        for event_index in expected_events:
            self.assertIn('info', self.parser.events[event_index])
            self.assertNotIn('Headers', self.parser.events[event_index])


if __name__ == '__main__':
    unittest.main()
