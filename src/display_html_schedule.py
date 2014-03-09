
from datetime import datetime

import talk
from display_utils import HTMLSchedule, Schedule


match_data = talk.command_yaml('list-matches 2013-01-01 2014-01-01')
match_data = match_data['matches']

MAX_MATCHES = 10

now = datetime(2013, 04, 13, hour = 15)
date = now.date()
match_count = 0

def dt_filter(then):
    global date, match_count
    if then.date() != date:
        return False
    if then < now:
        return False
    match_count += 1
    return match_count <= MAX_MATCHES

schedule = Schedule(match_data)
html_schedule = HTMLSchedule(schedule)
print html_schedule.get_table(headings = False, full_names = False, dt_filter = dt_filter)
