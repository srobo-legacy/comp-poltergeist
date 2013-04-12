
import config

import talk
from display_utils import format_name

config.load_config()

team_data = talk.command_yaml('list-teams')
team_list = team_data['list']

QUALIFYING_TEAMS = 24

print '''//TITLE: 2013 Competition League

# League Status

| Position | Points | Team |
|----------|--------|------|'''

pos = 1

for tla, name in team_list.iteritems():
    league_data = talk.command_yaml('get-league-points {0}'.format(tla))
    pts = league_data['points']
    pts = pts if pts else 0
    team = format_name(tla, name)

    if pos == QUALIFYING_TEAMS + 1:
        print '| - | - | - |'

    print "| {0} | {1} | {2} |".format(pos, pts, team)
    pos += 1
