
import config

import talk
from datetime import datetime
from display_utils import get_team_name, format_name, get_delayed_time

config.load_config()

match_data = talk.command_yaml('list-matches 2013-04-12 2014-01-01')
match_data = match_data['matches']

print '''//TITLE: 2013 Match Schedule
//CONTENT_TYPE: html

<h1> Match Schedule </h1>
'''

def get_header(date):
    out = '\n<h2>{0}</h2>'.format(date.strftime('%A, %d %B %Y'))
    out += '\n<table class="match-schedule"><thead><tr>'
    out += '\n<th> Time </th><th> Match </th><th> Zone 0 </th><th> Zone 1 </th><th> Zone 2 </th><th> Zone 3 </th>'
    out += '\n</tr></thead><tbody>'
    return out

def get_tail():
    return '</tbody></table>'

def get_team_cell(team_id, show_name = False):
    name = get_team_name(team_id)
    if show_name:
        id_html = '<span class="team-id">{0}</span>'.format(team_id)
        name_html = '<span class="team-name">{0}</span>'.format(name)
        text = format_name(id_html, name_html)
    else:
        text = '<span class="team-id" title="{1}">{0}</span>'.format(team_id, name)

    return '<td class="team-{0}">{1}</td>'.format(team_id, text)

def get_row(time, num, teams, show_team_name = False):
    out = '\n<tr class="match-{0}">'.format(int(num))
    cells = [get_team_cell(tid, show_team_name) for tid in teams]
    out += "\n\t<td>{0}</td><td>{1}</td>{2}".format(time, num, ''.join(cells))
    out += "\n</tr>"
    return out

date = None

for ident, stamp in match_data:
    dt = datetime.fromtimestamp(stamp)
    dt = get_delayed_time(dt)
    teams_data = talk.command_yaml('get-match-teams {0}'.format(ident))
    #print teams_data
    team_ids = teams_data['teams']
    this_date = dt.date()
    if date != this_date:
        if date is not None:
            print get_tail()
        date = this_date
        print get_header(date)
    num = ident[6:]
    print get_row(dt.time(), num, team_ids, True)

print get_tail()
