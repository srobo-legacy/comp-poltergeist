
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

date = None

# FIXME: the first match data is problematic!
for ident, stamp in match_data[1:]:
    dt = datetime.fromtimestamp(stamp)
    teams_data = talk.command_yaml('get-match-teams {0}'.format(ident))
    #print teams_data
    team_ids = teams_data['teams']
    teams = [get_team_name(t) for t in team_ids]
    this_date = dt.date()
    if date != this_date:
        date = this_date
        print
        print '##', date
        print '| Time | Match | Zone 0 | Zone 1 | Zone 2 | Zone 3 |'
        print '|------|-------|-------|'

    num = ident[6:]
    print "| {0} | {1} | {2} |".format(dt.time(), num, ' | '.join(teams))
