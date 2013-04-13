
from collections import defaultdict
import config

import talk
from display_utils import get_sorted_league_points

MAX_POS = 10

config.load_config()

QUALIFYING_TEAMS = 24

print '<table><tr>'
print '<th> Position </th><th> Points </th><th> Team </th>'
print '</tr><tr>'

pos = 1
sorted_tuples = get_sorted_league_points()

for pts, tla in sorted_tuples:
    if pos == QUALIFYING_TEAMS + 1:
        print '<td> - </td><td> - </td><td> - </td>'

    print "<td> {0} </td><td> {1} </td><td> {2} </td>".format(pos, pts, tla)
    pos += 1
    if pos > MAX_POS:
        break
    print '</tr><tr>'

print '</tr></table>'
