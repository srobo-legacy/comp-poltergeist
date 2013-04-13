
import config

import talk
from datetime import datetime
from display_utils import get_team_name

config.load_config()

match_data = talk.command_yaml('list-matches 2013 2014')
match_data = match_data['matches']

print '''//TITLE: 2013 Match Schedule

# Match Schedule
'''

MAX_TEAMS_PER_MATCH = 4

date = None
fail = False

for ident, stamp in match_data:
    scores_data = talk.command_yaml('get-scores {0}'.format(ident))
    scores = scores_data['scores']
    teams = set(scores.keys())
    dsq_data = talk.command_yaml('get-dsqs {0}'.format(ident))
    dsqs = set(dsq_data['dsqs']

    if len(teams) > MAX_TEAMS_PER_MATCH:
        print >>sys.stderr, "Too many teams in {0}".format(ident)

    active_teams = teams - dsqs
    if len(active_teams) > MAX_TEAMS_PER_MATCH:
        print >>sys.stderr, "Too many teams have scores in {0}".format(ident)
        fail = True

if fail:
    exit(1)
