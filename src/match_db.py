"""Match schedule database."""

import time

class MatchDB(object):
    """A match database."""

    def __init__(self, redis_connection):
        """Creates a new database wrapper around the given connection."""
        self._conn = redis_connection

    def create_match(self, name, time, format = 'league'):
        """Schedule a match. name should be a unique idenitifier for the
        match, time should be a unix timestamp for the start of the match."""
        self._conn.set('match:matches:{0}:format'.format(name), format)
        self._conn.zadd('match:schedule', time, name)
        self._conn.publish('match:schedule', 'update')

    def cancel_match(self, name):
        """Cancel a match."""
        self._conn.delete('match:matches:{0}:format'.format(name))
        self._conn.zrem('match:schedule', name)
        self._conn.publish('match:schedule', 'update')

    def set_teams(self, name, teams):
        """Set the teams for a match."""
        self._conn.delete('match:matches:{0}:teams'.format(name))
        if teams is not None:
            for team in teams:
                self._conn.rpush('match:matches:{0}:teams'.format(name),
                                                    team)
        self._conn.publish('match:schedule', 'update')


    def get_teams(self, name):
        """Get the teams for a match."""
        n_teams = self._conn.llen('match:matches:{0}:teams'.format(name))
        teams = self._conn.lrange('match:matches:{0}:teams'.format(name), 0, n_teams-1)
        return teams

    def matches_between(self, start, end):
        """Get events between a given start and end point, each specified
        as a unix timestamp.

        Returns a list of (name, timestamp) pairs."""
        return self._conn.zrangebyscore('match:schedule',
                                        start,
                                        end,
                                        withscores=True)

    def get_delay(self, when = None):
        """Gets the delay at the given point in time, specified as a unix
        timestamp, defaulting to the current delay.

        Returns an integer representing the delay in seconds."""
        if when is None:
            when = int(time.time())

        delays = self._conn.zrangebyscore('match:delays', 0, when)
        if len(delays):
            return delays[-1][0]
        return 0

    def set_delay(self, delay, when = None):
        """Sets the delay in seconds at the given point in time, specified
        as a unix timestamp, defaulting to the current delay."""
        if when is None:
            when = int(time.time())
        self._conn.zadd('match:delays', when, delay)
