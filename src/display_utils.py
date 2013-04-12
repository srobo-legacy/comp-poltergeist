
import talk

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
