"""
Test suite for CloverleafParser
"""
import unittest
from cloverleaf_parser import CloverleafParser


class TestCloverleafParser(unittest.TestCase):
    def setUp(self):
        self.parser = CloverleafParser()
        self.example_logfile = "test/test.log"
        with open(self.example_logfile) as f:
            self.parser.parse(f)

    def tearDown(self):
        pass

    def test_initialization(self):
        self.assertEqual(len(self.parser.events), 6)

    def test_can_parse_example_file(self):
        self.assertEqual(len(self.parser.events), 6)

        expected_events = [
            # event 1
            {'time': 'Jan 22, 2020 12:34:27 AM',
                'direction': 'Inbound Message',
                'info': {'clientport': '14290',
                    'pathinfo': '/sync',
                    'requestURL': 'http://10.3.17.233:8200/sync',
                    'query': 'last_event_id=f744fccf1cb2952fab8b',
                    'path': '/sync',
                    'clientip': '10.251.15.10',
                    'method': 'GET'},
                'handle': 'com.infor.cloverleaf.gjdws.handlers.RawHandler',
                'Message Content': {},
                'Incoming Request Header Information': {
                    'Content-Length': '0',
                    'Accept-Encoding': 'gzip',
                    'Accept': 'application/vnd.doctolib.v1+json',
                    'User-Agent': 'SAP NetWeaver Application Server (1.0;750)',
                    'Host': '10.3.17.233:8200',
                    'Date': 'Tue, 21 Jan 2020 23:34:27 GMT',
                    'Content-MD5': '1B2M2Y8AsgTpgAmY7PhCfg==',
                    'Content-Type': 'text/html',
                    'Authorization': 'APIAuth 987:+wewODVlgLJeoFuDV1/2p0DrHLU='}
            },
            # event 2
            {
                'info': {},
                'direction': 'Outbound Message',
                'Response message content': {
                    'text': '{"events":[]}'
                },
                'handle': 'com.infor.cloverleaf.gjdws.handlers.RawHandler',
                'Headers': {
                    'Expect-CT': 'max-age=604800, report-uri=&quot;https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct&quot;',
                    'X-Request-Id': '52e4abb0689a2d80f022abb3be8016fa',
                    'X-XSS-Protection': '1; mode=block',
                    'X-Download-Options': 'noopen',
                    'X-Content-Type-Options': 'nosniff',
                    'transfer-encoding': 'chunked',
                    'Set-Cookie': '__cfduid=d06fa3c40b9cf6aee8de73ada7694a8c71579649668; expires=Thu, 20-Feb-20 23:34:28 GMT; path=/; domain=.doctolib.de; HttpOnly; SameSite=Lax',
                    'CF-Cache-Status': 'DYNAMIC',
                    'Strict-Transport-Security': 'max-age=15724800; includeSubDomains',
                    'Vary': 'Accept-Encoding',
                    'connection': 'keep-alive',
                    'Server': 'cloudflare',
                    'X-Runtime': '0.028273',
                    'ETag': 'W/&quot;24de1c4a19c43ad41b013f13dcd858c1&quot;',
                    'X-Permitted-Cross-Domain-Policies': 'none',
                    'Cache-Control': 'max-age=0, private, must-revalidate',
                    'Date': 'Tue, 21 Jan 2020 23:34:28 GMT',
                    'CF-RAY': '558d1958fc6a7e91-MUC',
                    'Referrer-Policy': 'strict-origin-when-cross-origin',
                    'Content-Type': 'application/json; charset=utf-8',
                    'X-Frame-Options': 'SAMEORIGIN'
                },
                'time': 'Jan 22, 2020 12:34:28 AM',
                'Response information': {
                    'Response Code': '200'
                }
            },
            # event 3
            {
                'time': 'Jan 22, 2020 1:34:28 AM'
            },
            # event 4
            {
                'time': 'Jan 22, 2020 1:34:28 AM',
                'Response information': {
                    'Response Code': '201'
                }
            },
            # event 5
            {
                'time': 'Jan 22, 2020 1:34:28 AM'
            },
            # event 6
            {
                'time': 'Jan 22, 2020 1:34:28 AM',
                'Response information': {
                    'Response Code': '400'},
                'Response message content': {
                    'text': '{"error":"invalid_json","error_messages":["Impossible de parser le contenu du message au format JSON."]}'
                }
            }]
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

    def test_filter(self):
        filter = lambda key, value: key.lower() in ('response')

if __name__ == '__main__':
    unittest.main()
