"""Team commands."""

import re
import yaml

import control
import redis_client
from team_db import TeamDB

roster = TeamDB(redis_client.connection)
yaml_opt = '--yaml'

@control.handler('team')
def perform_team(responder, options):
    tla = options['<tla>']
    team = roster.get(options['<tla>'])

    if options.get(yaml_opt, False):
        responder(yaml.dump({'team': team}))
        return

    responder('{0}: {1}'.format(tla, team['name']))
    responder('    College: {0}'.format(team['college']))
    responder('    ' + ('PRESENT' if team['present'] else 'ABSENT'))
    if team['notes']:
        responder(str(team['notes']))

@control.handler('list-teams')
def perform_list_teams(responder, options):
    list = roster.list()

    if not list:
        if options.get(yaml_opt, False):
            responder(yaml.dump({'list': list}))
        else:
            responder('No teams in database.')
        return

    names_list = []
    for tla in list:
        info = roster.get(tla)
        if not options.get(yaml_opt, False):
            responder('{0}: {1}'.format(tla, info['name']))
        else:
            names_list.append(info['name'])

    if options.get(yaml_opt, False):
        teams_data = dict(zip(list, names_list))
        responder(yaml.dump({'list': teams_data}))

@control.handler('add-team')
def perform_add_team(responder, options):
    roster.add(options['<tla>'],
               options['<college>'],
               options['<name>'])
    responder('Team {0} added.'.format(options['<tla>']))

@control.handler('del-team')
def perform_del_team(responder, options):
    roster.delete(options['<tla>'])
    responder('Team {0} dropped.'.format(options['<tla>']))

@control.handler('set-team-present')
def perform_set_team_present(responder, options):
    roster.mark_present(options['<tla>'])
    responder('Team {0} marked present.'.format(options['<tla>']))

@control.handler('set-team-absent')
def perform_set_team_absent(responder, options):
    roster.mark_absent(options['<tla>'])
    responder('Team {0} marked absent.'.format(options['<tla>']))

@control.handler('set-team-name')
def perform_set_team_name(responder, options):
    roster.update(options['<tla>'],
                  name = options['<name>'])
    responder('Team {0} updated.'.format(options['<tla>']))

@control.handler('set-team-college')
def perform_set_team_college(responder, options):
    roster.update(options['<tla>'],
                  college = options['<college>'])
    responder('Team {0} updated.'.format(options['<tla>']))

@control.handler('set-team-notes')
def perform_set_team_notes(responder, options):
    roster.update(options['<tla>'],
                  notes = options['<notes>'])
    responder('Team {0} updated.'.format(options['<tla>']))

@control.handler('append-note')
def perform_append_notes(responder, options):
    team = roster.get(options['<tla>'])
    notes = team['notes']
    # add a full stop if there isn't one
    if notes == None:
        notes = ""
    elif notes and notes[-1] not in '.?!':
        notes += '.'
    notes += ' {0}'.format(options['<note>'])
    roster.update(options['<tla>'],
                  notes = notes)
    responder('Team {0} notes updated.'.format(options['<tla>']))

