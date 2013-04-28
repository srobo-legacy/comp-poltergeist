
import config

import talk
from datetime import datetime
from display_utils import HTMLSchedule, Schedule

config.load_config()

match_data = talk.command_yaml('list-matches 2013-04-12 2014-01-01')
match_data = match_data['matches']

print '''//TITLE: 2013 Match Schedule
//CONTENT_TYPE: html

'''

location_data = {'SWI': 'Level 3', 'TWG': 'Concourse', 'EMM': 'Level 2', 'RES': 'Concourse', 'CRB': 'Level 3', 'HRS2': 'Level 3', 'BGR': 'Level 2', 'BPV': 'Level 2', 'SEN2': 'Level 2', 'CPR': 'Level 2', 'BAM': 'Level 2', 'STA': 'Level 3', 'BWS': 'Level 2', 'MFG': 'Level 2', 'JMS': 'Level 3', 'HSO': 'Level 2', 'PSC2': 'Concourse', 'SEN': 'Level 2', 'QMC': 'Concourse', 'HSO2': 'Level 2', 'GRS': 'Level 3', 'CLF': 'Concourse', 'HRS': 'Level 3', 'GRD': 'Concourse', 'spare': 'Pod 1', 'CLY': 'Level 2', 'GMR': 'Pod 1', 'PSC': 'Concourse', 'HZW': 'Level 2', 'PLE': 'Concourse', 'BRK': 'Concourse', 'QEH': 'Concourse', 'MAI': 'Level 2', 'ALT': 'Level 3'}

schedule = Schedule(match_data)
html_schedule = HTMLSchedule(schedule, location_data)
print html_schedule.get_all()
