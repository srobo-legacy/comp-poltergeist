
import config

import talk
import dateutil.parser

config.load_config()

match_data = talk.command('list-matches 2013 2014')
match_list = match_data.strip().split("\n")

print '''//TITLE: 2013 Match Schedule

# Match Schedule
'''

date = None

for line in match_list:
    dt_str, ident = line.rsplit(':', 1)
    dt = dateutil.parser.parse(dt_str)
    teams_data = talk.command_yaml('get-match-teams {0}'.format(ident))
    teams = teams_data['teams']
    this_date = dt.date()
    if date != this_date:
        date = this_date
        print
        print '##', date
        print '| Time | Match | Teams |'
        print '|------|-------|-------|'

    print "| {0} | {1} | {2} |".format(dt.time(), ident, ', '.join(teams))
