
import datetime
import time

import utils

# Unit tests

## ScoresDB access

def assertEqual(expected, actual):
    assert expected == actual, "\nExpected: {0}\n  Actual: {1}".format(expected, actual)

def test_parse_time_0():
    human = '2011-04-03'
    expected = datetime.datetime(2011, 04, 03)
    actual_raw = utils.parse_time(human)
    actual = datetime.datetime.fromtimestamp(actual_raw)
    assertEqual(expected, actual)

def test_parse_time_1():
    human = '2011-04-03T00:00'
    expected = datetime.datetime(2011, 04, 03)
    actual_raw = utils.parse_time(human)
    actual = datetime.datetime.fromtimestamp(actual_raw)
    assertEqual(expected, actual)

def test_parse_time_2():
    human = '2011-04-03T00:00:00'
    expected = datetime.datetime(2011, 04, 03)
    actual_raw = utils.parse_time(human)
    actual = datetime.datetime.fromtimestamp(actual_raw)
    assertEqual(expected, actual)

def test_parse_time_3():
    human = '2013-04-13T09:01'
    expected = datetime.datetime(2013, 04, 13, 9, 1)
    actual_raw = utils.parse_time(human)
    actual = datetime.datetime.fromtimestamp(actual_raw)
    assertEqual(expected, actual)

def test_time_parse():
    assert utils.parse_time('9:00') == 3600*9
    assert utils.parse_time('12:00') == 3600*12
    assert utils.parse_time('16:30') == 3600*16 + 60*30
    assert utils.parse_time('16:30:35') == 3600*16 + 60*30 + 35
    try:
        utils.parse_time('whenever')
        assert False
    except utils.ParseError:
        pass

def test_format_time():
    assert utils.format_time(3600*8 +
                             60*3 +
                             45) == '8:03:45'
