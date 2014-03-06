
from datetime import datetime, date, time
import mock
from time import mktime
import yaml

import match_commands

def stamp(hour = 0, minute = 0):
    dt = datetime.combine(date.today(), time(hour, minute))
    return mktime(dt.timetuple())

def test_get_delay_now():
    now = 142.1
    fake_time = mock.Mock(return_value = now)
    fake_matches = mock.Mock()
    delay = 60 # 1 minute
    fake_matches.get_delay = mock.Mock(return_value = delay)

    with mock.patch('time.time', fake_time), \
            mock.patch('match_commands.matches', fake_matches):
        responder = mock.Mock()
        match_commands.perform_get_delay(responder, {})

        expected = {'delay': delay, 'units': 'seconds'}
        responder.assert_called_once_with(yaml.dump(expected))

    fake_matches.get_delay.assert_called_once_with(int(now))

def test_get_delay_then():
    fake_time = mock.Mock(return_value = 142.1)
    then = stamp(13, 0)
    fake_matches = mock.Mock()
    delay = 600 # 10 minutes
    fake_matches.get_delay = mock.Mock(return_value = delay)

    with mock.patch('time.time', fake_time), \
            mock.patch('match_commands.matches', fake_matches):
        responder = mock.Mock()
        match_commands.perform_get_delay(responder, {'<when>': "13:00"})

        expected = {'delay': delay, 'units': 'seconds'}
        responder.assert_called_once_with(yaml.dump(expected))

    fake_matches.get_delay.assert_called_once_with(int(then))

def test_set_delay_now():
    now = 142.1
    fake_time = mock.Mock(return_value = now)
    fake_matches = mock.Mock()
    delay = 60 # 1 minute
    fake_matches.set_delay = mock.Mock(return_value = delay)

    with mock.patch('time.time', fake_time), \
            mock.patch('match_commands.matches', fake_matches):
        responder = mock.Mock()
        match_commands.perform_set_delay(responder, {'<delay>': delay})

        expected = 'delay set'
        responder.assert_called_once_with(expected)

    fake_matches.set_delay.assert_called_once_with(int(now), delay)

def test_set_delay_then():
    fake_time = mock.Mock(return_value = 142.1)
    then = stamp(13, 0)
    fake_matches = mock.Mock()
    delay = 600 # 10 minutes
    fake_matches.set_delay = mock.Mock(return_value = delay)

    with mock.patch('time.time', fake_time), \
            mock.patch('match_commands.matches', fake_matches):
        responder = mock.Mock()
        options = {'<delay>': delay, '<when>': "13:00"}
        match_commands.perform_set_delay(responder, options)

        expected = 'delay set'
        responder.assert_called_once_with(expected)

    fake_matches.set_delay.assert_called_once_with(int(then), delay)
