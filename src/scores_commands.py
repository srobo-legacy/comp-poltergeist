"""Team scores commands."""

import yaml

import control
import ranker
import redis_client
from scores_db import ScoresDB

scores = ScoresDB(redis_client.connection)
yaml_opt = '--yaml'

@control.handler('set-score')
def perform_set_score(responder, options):
    """Handle the `set-score` command."""
    match = options['<match-id>']
    tla = options['<tla>']
    score = options['<score>']
    scores.set_match_score(match, tla, score)
    responder('Scored {0} points for {1} in match {2}'.format(score, tla, match))

@control.handler('get-score')
def perform_get_score(responder, options):
    """Handle the `get-score` command."""
    match = options['<match-id>']
    tla = options['<tla>']
    score = scores.get_match_score(match, tla)

    if options.get(yaml_opt, False):
        responder(yaml.dump({'score': score}))
    else:
        responder('Team {0} scored {1} in match {2}'.format(tla, score, match))

@control.handler('get-scores')
def perform_get_scores(responder, options):
    """Handle the `get-scores` command."""
    match = options['<match-id>']
    all_scores = scores.get_match_scores(match)

    if options.get(yaml_opt, False):
        responder(yaml.dump({'scores': all_scores}))
    else:
        if all_scores is None:
            responder('No scores available for match {0}'.format(match))
        else:
            for tla, score in all_scores.iteritems():
                responder('Team {0} scored {1} in match {2}'.format(tla, score, match))

@control.handler('calc-league-points')
def perform_calc_league_points(responder, options):
    """Handle the `calc-league-points` command."""
    match = options['<match-id>']
    match_scores = scores.get_match_scores(match)

    if match_scores is None:
        if options.get(yaml_opt, False):
            responder(yaml.dump({'points': None}))
        else:
            responder('No scores available for match {0}'.format(match))
        return

    dsq_teams = scores.teams_disqualified_in_match(match)
    league_points = ranker.get_ranked_points(match_scores, dsq_teams)
    scores.set_league_points(match, league_points)

    if options.get(yaml_opt, False):
        responder(yaml.dump({'points': league_points}))
    else:
        for tla, pts in league_points.iteritems():
            responder('Team {0} earned {1} points from match {2}'.format(tla, pts, match))

@control.handler('get-league-points')
def perform_get_league_points(responder, options):
    """Handle the `get-league-points` command."""
    tla = options['<tla>']
    league_points = scores.get_league_points(tla)

    if league_points is None:
        if options.get(yaml_opt, False):
            responder(yaml.dump({'points': None}))
        else:
            responder('No scores available for team {0}'.format(tla))
        return

    if options.get(yaml_opt, False):
        responder(yaml.dump({'points': league_points}))
    else:
        responder('Team {0} have {1} league points'.format(tla, league_points))

@control.handler('get-dsqs')
def perform_get_dsqs(responder, options):
    """Handle the `get-dsqs` command."""
    match = options['<match-id>']
    dsqs = scores.teams_disqualified_in_match(match)
    if options.get(yaml_opt, False):
        responder(yaml.dump({'dsqs': dsqs}))
    else:
        if len(dsqs) == 0:
            responder('No teams were disqualified from match {0}'.format(match))
        else:
            dsqs_str = ', '.join(dsqs)
            responder('Team(s) {0} were disqualified from match {1}'.format(dsqs_str, match))

@control.handler('disqualify')
def perform_disqualify(responder, options):
    """Handle the `disqualify` command."""
    match = options['<match-id>']
    tla = options['<tla>']
    scores.disqualify(match, tla)
    responder('Disqualified {0} in match {1}'.format(tla, match))

@control.handler('re-qualify')
def perform_re_qualify(responder, options):
    """Handle the `re-qualify` command."""
    match = options['<match-id>']
    tla = options['<tla>']
    scores.re_qualify(match, tla)
    responder('Re-qualified {0} in match {1}'.format(tla, match))
