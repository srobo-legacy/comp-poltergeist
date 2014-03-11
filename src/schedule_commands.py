"""Day schedule commands."""

import control
from poltergeist import redis_client
from schedule_db import ScheduleDB, EVENT_TYPES
from utils import format_time, parse_time

schedule = ScheduleDB(redis_client.connection)

@control.handler('schedule')
def perform_schedule(responder, options):
    """Handle the `schedule` command."""
    try:
        time = parse_time(options['<time>'])
    except ValueError:
        responder('Sorry, I didn\'t understand that time')
        return
    for type_ in EVENT_TYPES:
        if options[type_]:
            id_ = schedule.create_event(time, type_)
            responder('Scheduled as {0}'.format(id_))
            break
    else:
        responder('Not sure what event type that is?')

@control.handler('unschedule')
def perform_unschedule(responder, options):
    """Handle the `unschedule` command."""
    id_ = options['<id>']
    schedule.cancel_event(id_)
    responder('Done!')

@control.handler('show-schedule')
def perform_show_schedule(responder, options):
    """Handle the `show-schedule` command."""
    try:
        from_ = parse_time(options['<from>'])
        to_ = parse_time(options['<to>'])
    except ValueError:
        responder('Sorry, I didn\'t understand that time')
        return
    entries = schedule.events_between(from_, to_)
    for k, v in entries:
        responder('{0} - {1}'.format(format_time(v), k))
    if not entries:
        responder('No events in that time period')
