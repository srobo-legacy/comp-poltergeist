
import datetime
import match_db
import time

# Unit tests

## ScoresDB access

def assertEqual(expected, actual):
    assert expected == actual, "\nExpected: {0}\n  Actual: {1}".format(expected, actual)

def test_parse_time_0():
    human = '2011-04-03'
    expected = datetime.datetime(2011, 04, 03)
    actual_raw = match_db.parse_time(human)
    actual = datetime.datetime.fromtimestamp(actual_raw)
    assertEqual(expected, actual)

def test_parse_time_1():
    human = '2011-04-03T00:00:00'
    expected = datetime.datetime(2011, 04, 03)
    actual_raw = match_db.parse_time(human)
    actual = datetime.datetime.fromtimestamp(actual_raw)
    assertEqual(expected, actual)
