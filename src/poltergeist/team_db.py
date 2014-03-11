"""Team database."""

import re

class TeamDB(object):
    """A team database."""

    def __init__(self, redis_connection):
        """Creates a new database wrapper around the given connection."""
        self._conn = redis_connection

    def add(self, tla, college, name):
        """Add a team into the database."""
        self._conn.set('team:{0}:college'.format(tla), college)
        self._conn.set('team:{0}:name'.format(tla), name)
        # We initially have the notes empty to be filled in later
        self._conn.set('team:{0}:notes'.format(tla), '')
        # Fill in presence when teams arrive
        self._conn.set('team:{0}:present'.format(tla), False)
        self._conn.publish('team:update', 'update')

    def delete(self, tla):
        """Delete a team from the database entirely.

        This is probably not what you want unless you added one by accident."""
        # Remove all keys
        for key in ('college', 'name', 'notes', 'present'):
            self._conn.delete('team:{0}:{1}'.format(tla, key))
        # TODO: interact with other systems
        self._conn.publish('team:update', 'update')

    def update(self, tla, college = None, name = None, notes = None):
        """Update team details in the DB."""
        for key, value in {'college': college,
                           'name': name,
                           'notes': notes}.iteritems():
            if value is None:
                continue
            self._conn.set('team:{0}:{1}'.format(tla, key), value)
        self._conn.publish('team:update', 'update')

    # Presence is used, among other things, for determining whether a team
    # will be included in the match scheduling pool.
    def mark_present(self, tla):
        """Mark a given team present."""
        # TODO: check the team actually exists
        self._conn.set('team:{0}:present'.format(tla), True)
        self._conn.publish('team:update', 'update')

    def mark_absent(self, tla):
        """Mark a given team absent."""
        # TODO: check the team actually exists
        self._conn.set('team:{0}:present'.format(tla), False)
        self._conn.publish('team:update', 'update')

    def list(self):
        # Take a census of team:*:college keys
        keys = self._conn.keys('team:*:college')
        teams = [re.match('team:([a-zA-Z0-9]*):college', key).group(1)
                             for key in keys]
        return teams

    def get(self, team):
        # Return team info dict
        keys = ['team:{0}:{1}'.format(team, x)
                   for x in ('college', 'name', 'notes', 'present')]
        college, name, notes, present = self._conn.mget(*keys)

        info = {'college': college,
                'name': name,
                'notes': notes,
                'present': present}
        return info
