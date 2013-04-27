
import config

import talk
from datetime import datetime
from display_utils import HTMLSchedule

config.load_config()

match_data = talk.command_yaml('list-matches 2013-04-12 2014-01-01')
match_data = match_data['matches']

print '''//TITLE: 2013 Match Schedule
//CONTENT_TYPE: html

'''

html_schedule = HTMLSchedule(match_data)
print html_schedule.get_all()
