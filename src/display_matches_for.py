#!/usr/bin/env python
import sys

from display_utils import HTMLSchedule, Schedule
import talk

ALL_OPT = '--all'

if len(sys.argv) != 2:
    print >> sys.stderr, "Usage: display_matches_for.py (TEAM|--all)"
    exit(1)

req_team = sys.argv[1]

all_teams = talk.command_yaml('list-teams')
all_teams = all_teams['list']
team_ids = all_teams.keys()

if not (req_team in team_ids or req_team == ALL_OPT):
    print >> sys.stderr, "Unknown team '{0}'.".format(req_team)
    exit(2)

# TODO: remove need for arguments when requesting all the matches
match_data = talk.command_yaml('list-matches 2013-01-01 2014-01-01')
match_data = match_data['matches']

def get_team_filter(filter_team):
    def team_filter(teams):
        return filter_team in teams
    return team_filter

schedule = Schedule(match_data)
html_schedule = HTMLSchedule(schedule)

if req_team == ALL_OPT:
    for team in team_ids:
        with open(team, 'w') as f:
            print >> f, html_schedule.get_table(team_filter = get_team_filter(team))
else:
    print html_schedule.get_table(team_filter = get_team_filter(req_team))
