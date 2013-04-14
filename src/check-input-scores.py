
from datetime import datetime
import sys

from display_utils import get_team_name
import config
import talk

config.load_config()

MAX_TEAMS_PER_MATCH = 4

match_data = talk.command_yaml('list-matches 2013-01-01 2014-01-01')
match_data = match_data['matches']

date = None
fail = False

for ident, stamp in match_data:
    scores_data = talk.command_yaml('get-scores {0}'.format(ident))
    scores = scores_data['scores']
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

if fail:
    exit(1)
