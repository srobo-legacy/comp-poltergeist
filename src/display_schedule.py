
import config

import talk
from datetime import datetime
from display_utils import get_team_name, get_delayed_time

config.load_config()

match_data = talk.command_yaml('list-matches 2013-04-12 2014-01-01')
match_data = match_data['matches']

print '''//TITLE: 2013 Match Schedule

<h1> Match Schedule </h1>
'''

def get_header(date):
    out = '\n<h2>{0}</h2>'.format(date.strftime('%A, %d %B %Y'))
    out += '\n<table><thead><tr>'
    out += '\n<th> Time </th><th> Match </th><th> Zone 0 </th><th> Zone 1 </th><th> Zone 2 </th><th> Zone 3 </th>'
    out += '\n</tr></thead><tbody>'
    return out

def get_tail():
    return '</tbody></table>'

def get_row(time, match, teams):
    out = "\n<tr>"
    out += "\n\t<td>{0}</td><td>{1}</td><td>{2}</td>".format(time, match, '</td><td>'.join(teams))
    out += "\n</tr>"
    return out

date = None

for ident, stamp in match_data:
    dt = datetime.fromtimestamp(stamp)
    dt = get_delayed_time(dt)
    teams_data = talk.command_yaml('get-match-teams {0}'.format(ident))
    #print teams_data
    team_ids = teams_data['teams']
    teams = [get_team_name(t) for t in team_ids]
    this_date = dt.date()
    if date != this_date:
        if date is not None:
            print get_tail()
        date = this_date
        print get_header(date)
    num = ident[6:]
    print get_row(dt.time(), num, teams)

print get_tail()
