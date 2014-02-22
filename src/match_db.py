"""Match schedule database."""

import redis_client
import control
import re
import yaml

from utils import format_time, parse_time

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

matches = MatchDB(redis_client.connection)
yaml_opt = '--yaml'

@control.handler('add-match')
def perform_add_match(responder, options):
    matches.create_match(options['<name>'],
                         parse_time(options['<time>']),
                         'knockout' if options['--knockout'] else 'league')
    responder('Match {0} scheduled.'.format(options['<name>']))

@control.handler('del-match')
def perform_del_match(responder, options):
    matches.cancel_match(options['<name>'])
    responder('Match {0} canceled.'.format(options['<name>']))

@control.handler('set-match-teams')
def perform_set_match_teams(responder, options):
    matches.set_teams(options['<name>'],
                      options['<team>'])
    responder('Teams set.')

@control.handler('get-match-teams')
def perform_get_match_teams(responder, options):
    match = options['<match-id>']
    teams = matches.get_teams(match)
    if options.get(yaml_opt, False):
        responder(yaml.dump({'teams': teams}))
    else:
        if len(teams) == 0:
            responder('No teams are in match {0}'.format(match))
        else:
            teams_str = ', '.join(teams)
            responder('Team(s) {0} are in match {1}'.format(teams_str, match))

@control.handler('clear-match-teams')
def perform_clear_match_teams(responder, options):
    matches.set_teams(options['<name>'], '')
    responder('Teams cleared.')

@control.handler('list-matches')
def perform_list_matches(responder, options):
    fr = parse_time(options['<from>'])
    to = parse_time(options['<to>'])
    output = matches.matches_between(fr, to)

    if options.get(yaml_opt, False):
        responder(yaml.dump({'matches': output}))
        return

    if not output:
        responder('No matches.')
    else:
        for match, time in output:
            responder('{0}: {1}'.format(format_time(time), match))

