
from collections import defaultdict
import config

import talk
from display_utils import format_name

def gen_pts_tla(points_sorted, points_map):
    for pts in points_sorted:
        for tla in points_map[pts]:
            yield pts, tla

config.load_config()

team_data = talk.command_yaml('list-teams')
team_list = team_data['list']

QUALIFYING_TEAMS = 24

print '''//TITLE: 2013 Competition League

# League Status

| Position | Points | Team |
|----------|--------|------|'''

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
        print '| - | - | - |'

    print "| {0} | {1} | {2} |".format(pos, pts, team)
    pos += 1
