
import mock

import match_db

def test_get_delay_now():
    now = 142.1
    fake_time = mock.Mock(return_value = now)
    fake_connection = mock.Mock()
    delays = [(10, 42), (50, 65)]
    fake_connection.zrangebyscore = mock.Mock(return_value = delays)

    matches = match_db.MatchDB(fake_connection)

    with mock.patch('time.time', fake_time):
        delay = matches.get_delay()
        assert delay == 50, "Should have returned the latest delay value"

    fake_connection.zrangebyscore.assert_called_once_with('match:delays', 0, int(now))

def test_get_delay_then():
    then = 142
    fake_connection = mock.Mock()
    delays = [(10, 42), (51, 65)]
    fake_connection.zrangebyscore = mock.Mock(return_value = delays)

    matches = match_db.MatchDB(fake_connection)

    delay = matches.get_delay(then)
    assert delay == 51, "Should have returned the latest delay value"

    fake_connection.zrangebyscore.assert_called_once_with('match:delays', 0, then)

def test_get_delay_then_none():
    then = 142
    fake_connection = mock.Mock()
    delays = []
    fake_connection.zrangebyscore = mock.Mock(return_value = delays)

    matches = match_db.MatchDB(fake_connection)

    delay = matches.get_delay(then)
    assert delay == 0, "Should have returned 0 when there were no delays"

    fake_connection.zrangebyscore.assert_called_once_with('match:delays', 0, then)

def test_set_delay_now():
    now = 1111142.1
    fake_time = mock.Mock(return_value = now)
    fake_connection = mock.Mock()
    fake_connection.zadd = mock.Mock()

    matches = match_db.MatchDB(fake_connection)

    delay = 60 # 1 minute
    with mock.patch('time.time', fake_time):
        matches.set_delay(delay)

    fake_connection.zadd.assert_called_once_with('match:delays', int(now), delay)

def test_set_delay_then():
    then = 1111145
    fake_connection = mock.Mock()
    fake_connection.zadd = mock.Mock()

    matches = match_db.MatchDB(fake_connection)

    delay = 90 # 1 minute 30
    matches.set_delay(delay, then)
    fake_connection.zadd.assert_called_once_with('match:delays', then, delay)
