
from datetime import datetime, date, time
import mock
from time import mktime

import control
import schedule_commands

def test_command_unschedule():
    mock_cancel = mock.Mock()
    with mock.patch('schedule_commands.schedule.cancel_event', mock_cancel):
        control.handle('unschedule eyes')
    mock_cancel.assert_called_once_with('eyes')

def stamp(hour = 0, minute = 0):
    dt = datetime.combine(date.today(), time(hour, minute))
    return mktime(dt.timetuple())

def test_command_schedule():
    responder = mock.Mock()
    noon = stamp(12, 00)
    create_event = mock.Mock(return_value = 'eyes')
    with mock.patch('schedule_commands.schedule.create_event', create_event):
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
    with mock.patch('schedule_commands.schedule.events_between', events_between):
        control.handle('show-schedule moo 12:00', responder)
        responder.assert_called_once_with("Sorry, I didn't understand that time")
        responder.reset_mock()
        control.handle('show-schedule 9:00 13:00', responder)
        events_between.assert_called_once_with(nine_am, one_pm)
        responder.assert_called_once_with(today_iso8601 + ' 10:00:00 - eyes')
        responder.reset_mock()

    events_between = mock.Mock(return_value = [])
    with mock.patch('schedule_commands.schedule.events_between', events_between):
        control.handle('show-schedule 9:00 13:00', responder)
        events_between.assert_called_once_with(nine_am, one_pm)
        responder.assert_called_once_with('No events in that time period')
