
from collections import defaultdict

from display_utils import get_all_league_rows
import talk

MAX_POS = 10

QUALIFYING_TEAMS = 24

print '<table><tr>'
print '<th> Position </th><th> Points </th><th> Team </th>'

pos = 1
sorted_tuples = get_all_league_rows(MAX_POS)

for pts, tla, pos in sorted_tuples:
    print '</tr><tr>'
    if pos == QUALIFYING_TEAMS + 1:
        print '<td> - </td><td> - </td><td> - </td>'
        print '</tr><tr>'

    print "<td> {0} </td><td> {1} </td><td> {2} </td>".format(pos, pts, tla)

print '</tr></table>'
