"""Day schedule database."""

from uuid import uuid4

from poltergeist.utils import format_time, parse_time

EVENT_TYPES = ('league', 'knockout', 'lunch', 'open',
               'tinker', 'photo', 'prizes', 'briefing')

def create_id(prefix):
    """Create a unique event ID. The prefix should specify the type of
    event, one of EVENT_TYPES."""
    return '{0}-{1}'.format(prefix, str(uuid4())[:13])

class ScheduleDB(object):
    """A schedule database."""

    def __init__(self, redis_connection):
        """Creates a new database wrapper around the given connection."""
        self._conn = redis_connection

    def create_event(self, time, type_):
        """Schedule an event in the day. time should be given as a unix
        timestamp, and type_ should be one of EVENT_TYPES.

        Returns the ID of the event."""
        if type_ not in EVENT_TYPES:
            raise ValueError('unknown event type')
        id_ = create_id(type_)
        self._conn.set('comp:events:{0}'.format(id_),
                                    type_)
        self._conn.zadd("comp:schedule", time, id_)
        self._conn.publish('comp:schedule', 'update')
        return id_

    def cancel_event(self, id_):
        """Cancel an event in the day's schedule."""
        self._conn.delete('comp:events:{0}'.format(id_))
        self._conn.zrem('comp:schedule', id_)
        self._conn.publish('comp:schedule', 'update')

    def events_between(self, start, end):
        """Get events between a given start and end point, each specified
        as a unix timestamp.

        Returns a list of (id, timestamp) pairs."""
        return self._conn.zrangebyscore('comp:schedule',
                                        start,
                                        end,
                                        withscores=True)
