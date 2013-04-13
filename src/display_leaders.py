
from collections import defaultdict
import config

import talk
from display_utils import format_name

def gen_pts_tla(points_sorted, points_map):
    for pts in points_sorted:
        for tla in points_map[pts]:
            yield pts, tla

MAX_POS = 10

config.load_config()

team_data = talk.command_yaml('list-teams')
team_list = team_data['list']

QUALIFYING_TEAMS = 24

print '<table><tr>'

pts_map = defaultdict(lambda: [])

for tla in team_list.keys():
    league_data = talk.command_yaml('get-league-points {0}'.format(tla))
    pts = league_data['points']
    pts = pts if pts else 0
    pts_map[pts].append(tla)

pts_list = sorted(pts_map.keys(), reverse=True)
pos = 1

for pts, tla in gen_pts_tla(pts_list, pts_map):
    team = format_name(tla, team_list[tla])

    if pos == QUALIFYING_TEAMS + 1:
        print '<td> - </td><td> - </td><td> - </td>'

    print "<td> {0} </td><td> {1} </td><td> {2} </td>".format(pos, pts, team)
    pos += 1
    if pos > MAX_POS:
        break
    print '</tr><tr>'

print '</tr></table>'
