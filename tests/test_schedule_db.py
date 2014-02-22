
from datetime import datetime, date, time
from time import mktime
import schedule_db
import mock
import control

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

def test_command_unschedule():
    mock_cancel = mock.Mock()
    with mock.patch('schedule_db.schedule.cancel_event', mock_cancel):
        control.handle('unschedule eyes')
    mock_cancel.assert_called_once_with('eyes')

def stamp(hour = 0, minute = 0):
    dt = datetime.combine(date.today(), time(hour, minute))
    return mktime(dt.timetuple())

def test_command_schedule():
    responder = mock.Mock()
    noon = stamp(12, 00)
    create_event = mock.Mock(return_value = 'eyes')
    with mock.patch('schedule_db.schedule.create_event', create_event):
        control.handle('schedule lunch moo', responder)
        responder.assert_called_once_with("Sorry, I didn't understand that time")
        responder.reset_mock()
        control.handle('schedule lunch 12:00', responder)
        responder.assert_called_once_with("Scheduled as eyes")
        create_event.assert_called_once_with(noon, 'lunch')

def test_command_show_schedule():
    responder = mock.Mock()
    nine_am = stamp(9, 00)
    ten_am = stamp(10, 00)
    one_pm = stamp(13, 00)
    today_iso8601 = date.today().isoformat()
    events_between = mock.Mock(return_value = [('eyes', ten_am)])
    with mock.patch('schedule_db.schedule.events_between', events_between):
        control.handle('show-schedule moo 12:00', responder)
        responder.assert_called_once_with("Sorry, I didn't understand that time")
        responder.reset_mock()
        control.handle('show-schedule 9:00 13:00', responder)
        events_between.assert_called_once_with(nine_am, one_pm)
        responder.assert_called_once_with(today_iso8601 + ' 10:00:00 - eyes')
        responder.reset_mock()

    events_between = mock.Mock(return_value = [])
    with mock.patch('schedule_db.schedule.events_between', events_between):
        control.handle('show-schedule 9:00 13:00', responder)
        events_between.assert_called_once_with(nine_am, one_pm)
        responder.assert_called_once_with('No events in that time period')
