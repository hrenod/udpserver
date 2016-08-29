from collections import OrderedDict
from unittest import main, TestCase
from converter import convert, timestamp, encode


class ConversionTestCase(TestCase):
    def test_wrong_date_format(self):
        with self.assertRaises(Exception):
            convert('[17.06.2016 12:30] Time to move')

    def test_conversion(self):
        self.assertEqual(convert('[17/06/2016 12:30] Time to move'),
                         '{"timestamp":1466166600,"message":"Time to move"}')

    def test_conversion_long(self):
        self.assertEqual(convert('[17/06/2016 12:30]' + ' Time to move' * 10),
                         '{"timestamp":1466166600,"message":"Time to move' + ' Time to move' * 9 + '"}')

    def test_multi_line(self):
        self.assertEqual(convert("[17/06/2016 12:30] Time to move\nto second line"),
                         '{"timestamp":1466166600,"message":"Time to move\\nto second line"}')


class TimestampTestCase(TestCase):
    def test_conversion(self):
        self.assertEqual(timestamp({'day': '17', 'hour': '12', 'minute': '30', 'year': '2016', 'month': '06'}),
                         1466166600)

    def test_conversion_integers(self):
        self.assertEqual(timestamp({'day': 17, 'hour': 12, 'minute': 30, 'year': 2016, 'month': 6}),
                         1466166600)

    def test_missing_fields(self):
        with self.assertRaises(Exception):
            timestamp({'hour': '12', 'minute': '30', 'year': '2016', 'month': '06'})


class EncodingTestCase(TestCase):
    def test_encoding(self):
        data = OrderedDict([
            ('timestamp', 1466166),
            ('message', 'Time to move'),
        ])

        self.assertEqual(encode(data),
                         '{"timestamp":1466166,"message":"Time to move"}')


if __name__ == '__main__':
    main()
