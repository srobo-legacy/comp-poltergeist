"""Day schedule database."""

from uuid import uuid4
import redis_client
import control
import re
import yaml

from utils import format_time, parse_time

class MatchDB(object):
    """A match database."""
    def __init__(self):
        """Default constructor."""
        pass

    def create_match(self, name, time, format = 'league'):
        """Schedule a match."""
        redis_client.connection.set('match:matches:{0}:format'.format(name),
                                    format)
        redis_client.connection.zadd('match:schedule', time, name)
        redis_client.connection.publish('match:schedule', 'update')

    def cancel_match(self, name):
        """Cancel an event in the day's schedule."""
        redis_client.connection.delete('match:matches:{0}:format'.format(name))
        redis_client.connection.zrem('match:schedule', name)
        redis_client.connection.publish('match:schedule', 'update')

    def set_teams(self, name, teams):
        """Set the teams for a match."""
        redis_client.connection.delete('match:matches:{0}:teams'.format(name))
        if teams is not None:
            for team in teams:
                redis_client.connection.rpush('match:matches:{0}:teams'.format(name),
                                                    team)
        redis_client.connection.publish('match:schedule', 'update')


    def get_teams(self, name):
        """Get the teams for a match."""
        n_teams = redis_client.connection.llen('match:matches:{0}:teams'.format(name))
        teams = redis_client.connection.lrange('match:matches:{0}:teams'.format(name), 0, n_teams-1)
        return teams

    def matches_between(self, start, end):
        """Get events between a given start and end point, specified in
        seconds from the start of the day.

        Returns a Twisted Deferred on (name, time) pairs."""
        return redis_client.connection.zrangebyscore('match:schedule',
                                                     start,
                                                     end,
                                                     withscores=True)

matches = MatchDB()
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

