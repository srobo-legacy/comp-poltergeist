
from collections import defaultdict

import display_utils
import talk

last_scored_match = display_utils.last_scored_match()
print '''//TITLE: 2013 Competition Game Points

# Game Points Totals

Up to date with scores from match {0}

| Team | Points |
|------|--------|'''.format(last_scored_match)

all_scores = display_utils.get_all_match_scores()

scores_map = defaultdict(lambda: 0)

for ident, scores in all_scores.iteritems():
    if scores is None:
        continue
    for tla, pts in scores.iteritems():
        scores_map[tla] += pts

all_teams = display_utils.get_team_list()
for tla in sorted(all_teams.keys()):
    pts = scores_map[tla]
    print "| {0} | {1} |".format(tla, pts)
