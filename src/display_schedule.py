
import config

import talk
import dateutil.parser
from display_utils import get_team_name

config.load_config()

match_data = talk.command('list-matches 2013 2014')
match_list = match_data.strip().split("\n")

print '''//TITLE: 2013 Match Schedule

# Match Schedule
'''

date = None

for line in match_list[1:]:
    #print line
    dt_str, ident = line.rsplit(':', 1)
    dt = dateutil.parser.parse(dt_str)
    teams_data = talk.command_yaml('get-match-teams {0}'.format(ident))
    #print teams_data
    team_ids = teams_data['teams']
    teams = [get_team_name(t) for t in team_ids]
    this_date = dt.date()
    if date != this_date:
        date = this_date
        print
        print '##', date
        print '| Time | Match | Teams |'
        print '|------|-------|-------|'

    print "| {0} | {1} | {2} |".format(dt.time(), ident, ',<br />'.join(teams))
