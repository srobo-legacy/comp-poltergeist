"""Match schedule commands."""

import re
import yaml

import control
from match_db import MatchDB
import redis_client
from utils import format_time, parse_time

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
