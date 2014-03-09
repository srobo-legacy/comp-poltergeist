
import talk
import display_utils

QUALIFYING_TEAMS = 24

last_scored_match = display_utils.last_scored_match()
print '''//TITLE: 2013 Competition League

# League Status

Up to date with scores from match {0}

| Position | Points | Team |
|----------|--------|------|'''.format(last_scored_match)

team_list = display_utils.get_team_list()
sorted_tuples = display_utils.get_all_league_rows()

row = 1
for pts, tla, pos in sorted_tuples:
    team = display_utils.format_name(tla, team_list[tla])

    if row == QUALIFYING_TEAMS + 1:
        print '| - | - | - |'

    print "| {0} | {1} | {2} |".format(pos, pts, team)
    row += 1
