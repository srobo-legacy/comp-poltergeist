#!/usr/bin/env python
from datetime import datetime
import sys

import talk

MAX_TEAMS_PER_MATCH = 4

match_data = talk.command_yaml('list-matches 2013-01-01 2014-01-01')
match_data = match_data['matches']

team_data = talk.command_yaml('list-teams')
all_teams = team_data['list'].keys()

date = None
fail = False

for ident, stamp in match_data:
    scores_data = talk.command_yaml('get-scores {0}'.format(ident))
    scores = scores_data['scores']
    teams_data = talk.command_yaml('get-match-teams {0}'.format(ident))
    team_ids = teams_data['teams']
    print 'Checking {0}'.format(ident)
    if scores is None:
        # No scores for this match - that's fine.
        continue
    teams = set(scores.keys())
    dsq_data = talk.command_yaml('get-dsqs {0}'.format(ident))
    dsqs = set(dsq_data['dsqs'])

    if len(teams) > MAX_TEAMS_PER_MATCH:
        print >>sys.stderr, "Too many teams in {0}".format(ident)

    active_teams = teams - dsqs
    if len(active_teams) > MAX_TEAMS_PER_MATCH:
        print >>sys.stderr, "Too many teams have scores in {0}".format(ident)
        fail = True

    for team in active_teams:
        if not team in team_ids:
            print >>sys.stderr, "Non-entrant team {0} have scores in {1}".format(team, ident)
            fail = True

        if not team in all_teams:
            print >>sys.stderr, "Non-existent team {0} have scores in {1}".format(team, ident)
            fail = True

if fail:
    exit(1)
