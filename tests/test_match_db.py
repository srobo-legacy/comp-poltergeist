
import mock

import match_db

def test_get_delay_then():
    then = 14200
    fake_connection = mock.Mock()
    delays = ['100', '51']
    fake_connection.zrangebyscore = mock.Mock(return_value = delays)

    matches = match_db.MatchDB(fake_connection)

    delay = matches.get_delay(then)
    assert delay == 51, "Should have returned the latest delay value"

    fake_connection.zrangebyscore.assert_called_once_with('match:delays', 0, then)

def test_get_delay_then_none():
    then = 14200
    fake_connection = mock.Mock()
    delays = []
    fake_connection.zrangebyscore = mock.Mock(return_value = delays)

    matches = match_db.MatchDB(fake_connection)

    delay = matches.get_delay(then)
    assert delay == 0, "Should have returned 0 when there were no delays"

    fake_connection.zrangebyscore.assert_called_once_with('match:delays', 0, then)

def test_set_delay_then():
    then = 1111145
    fake_connection = mock.Mock()
    fake_connection.zadd = mock.Mock()

    matches = match_db.MatchDB(fake_connection)

    delay = 90 # 1 minute 30
    matches.set_delay(then, delay)
    fake_connection.zadd.assert_called_once_with('match:delays', then, delay)
