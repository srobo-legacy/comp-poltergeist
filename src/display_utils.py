
from datetime import timedelta, date
from collections import defaultdict

import talk

# Set the delay of the current
DELAYS = {
    date(2013, 04, 13): timedelta(minutes = 6),
    date(2013, 04, 14): timedelta(minutes = 0)
}

# Over-estimate for optimisation
TOTAL_MATCHES = 150

_team_cache = {}
def get_team_name(tla):
    if tla not in _team_cache:
        team_data = talk.command_yaml('team {0}'.format(tla))
        #print tla, team_data
        name = team_data['team']['name']
        name = format_name(tla, name)
        _team_cache[tla] = name

    return _team_cache[tla]

def format_name(tla, name):
    if name is not None:
        name = '{0}: {1}'.format(tla, name)
    else:
        name = tla
    return name

def get_delayed_time(original):
    orig_date = original.date()
    delay = DELAYS.get(orig_date, timedelta(0))
    new_dt = original + delay
    return new_dt

_team_list = None
def get_team_list():
    global _team_list
    if _team_list is None:
        team_data = talk.command_yaml('list-teams')
        _team_list = team_data['list']

    return _team_list

def gen_pts_tla(points_sorted, points_map):
    for pts in points_sorted:
        for tla in points_map[pts]:
            yield pts, tla

def get_sorted_league_points():
    team_list = get_team_list()

    pts_map = defaultdict(lambda: [])

    for tla in team_list.keys():
        league_data = talk.command_yaml('get-league-points {0}'.format(tla))
        pts = league_data['points']
        pts = pts if pts else 0
        pts_map[pts].append(tla)

    pts_list = sorted(pts_map.keys(), reverse=True)
    pos = 1

    sorted_tuples = gen_pts_tla(pts_list, pts_map)
    return sorted_tuples

def get_all_league_rows(row_limit = None):
    tuples = get_sorted_league_points()
    row = 1
    last_pts = 0
    for pts, tla in tuples:
        pos = row
        if last_pts == pts:
            pos = ''
        else:
            last_pts = pts
        yield pts, tla, pos
        if row_limit is not None and row >= row_limit:
            break
        row += 1

def last_scored_match():

    for n in range(1, TOTAL_MATCHES + 1):
        scores = talk.command_yaml('get-scores match-{0}'.format(n))
        if scores['scores'] is None:
            return n - 1
    return n
