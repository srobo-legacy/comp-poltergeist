
import config

import talk
from datetime import datetime
from display_utils import get_team_name, get_delayed_time

config.load_config()


match_data = talk.command_yaml('list-matches 2013 2014')
match_data = match_data['matches']

print '<table><tr>'
print '<th> Time </th><th> Match </th><th> Zone 0 </th><th> Zone 1 </th><th> Zone 2 </th><th> Zone 3 </th>'

MAX_MATCHES = 10

now = datetime.now()
date = now.date()

i = 0

for ident, stamp in match_data:
    dt = datetime.fromtimestamp(stamp)
    dt = get_delayed_time(dt)
    if dt < now:
        continue
    teams_data = talk.command_yaml('get-match-teams {0}'.format(ident))

    team_ids = teams_data['teams']
    this_date = dt.date()
    # Don't show the following day
    if date != this_date:
        break

    if i >= MAX_MATCHES:
        break
    i += 1

    num = ident[6:]
    print '</tr><tr>'
    print "<td> {0} </td><td> {1} </td><td> {2} </td>".format(dt.time(), num, ' </td><td> '.join(team_ids))

print '</tr></table>'
