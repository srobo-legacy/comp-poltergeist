
import mock

import schedule_db

def test_new():
    uuid_handler = mock.Mock(return_value = 'eyes')
    fake_connection = mock.Mock()
    fake_connection.zadd = mock.Mock()
    fake_connection.set = mock.Mock()
    fake_connection.publish = mock.Mock()

    schedule_db.create_id = uuid_handler
    schedule = schedule_db.ScheduleDB(fake_connection)

    rv = schedule.create_event(100, 'lunch')
    assert rv == 'eyes'
    fake_connection.zadd.assert_called_once_with('comp:schedule',
                                         100, 'eyes')
    fake_connection.set.assert_called_once_with('comp:events:eyes',
                                        'lunch')
    fake_connection.publish.assert_called_once_with('comp:schedule',
                                        'update')
    fake_connection.zadd.reset_mock()
    fake_connection.set.reset_mock()
    # Test for invalid event types
    try:
        schedule.create_event(103, 'pony')
    except ValueError:
        # excellent, just make sure of things
        assert not fake_connection.zadd.called
        assert not fake_connection.set.called
        # it does not matter if comp:schedule is called
    else:
        assert False

def test_cancel():
    fake_connection = mock.Mock()
    fake_connection.delete = mock.Mock()
    fake_connection.zrem = mock.Mock()
    fake_connection.publish = mock.Mock()

    schedule = schedule_db.ScheduleDB(fake_connection)

    schedule.cancel_event('eyes')
    fake_connection.delete.assert_called_once_with('comp:events:eyes')
    fake_connection.zrem.assert_called_once_with('comp:schedule', 'eyes')
    fake_connection.publish.assert_called_once_with('comp:schedule',
                                                    'update')

def test_events_between():
    # should be passthrough
    uniq1, uniq2, uniq3 = object(), object(), object()
    fake_connection = mock.Mock()
    fake_connection.zrangebyscore = mock.Mock(return_value = uniq1)

    schedule = schedule_db.ScheduleDB(fake_connection)

    result = schedule.events_between(uniq2, uniq3)
    assert result is uniq1
    assert fake_connection.zrangebyscore.called_with('comp:schedule',
                                                     uniq2,
                                                     uniq3,
                                                     withscores=True)
