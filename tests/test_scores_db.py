
import scores_db
import mock
import control
import yaml

# Unit tests

## ScoresDB access

def test_set_scores():
    fake_connection = mock.Mock()
    fake_connection.set = mock.Mock()

    scores = scores_db.ScoresDB(fake_connection)

    scores.set_match_score(1, 'ABC', 12)
    fake_connection.set.assert_called_once_with('match:scores:1:ABC:game', 12)

def test_set_league_points():
    fake_connection = mock.Mock()
    fake_connection.mset = mock.Mock()

    scores = scores_db.ScoresDB(fake_connection)

    raw_data = {'ABC':1.0, 'DEF':2.0}
    scores.set_league_points(1, raw_data)
    call_data = {'match:scores:1:ABC:league':1.0, 'match:scores:1:DEF:league':2.0}
    fake_connection.mset.assert_called_once_with(call_data)

def test_set_league_points():
    fake_connection = mock.Mock()
    fake_connection.mset = mock.Mock()

    scores = scores_db.ScoresDB(fake_connection)

    raw_data = {'ABC':1.0, 'DEF':2.0}
    scores.set_league_points(1, raw_data)
    call_data = {'match:scores:1:ABC:league':1.0, 'match:scores:1:DEF:league':2.0}
    fake_connection.mset.assert_called_once_with(call_data)

def test_get_league_points():
    fake_connection = mock.Mock()
    keys = ['match:scores:1:ABC:league', 'match:scores:2:ABC:league']
    fake_connection.keys = mock.Mock(return_value = keys)
    fake_points = [2.0, 3.0]
    fake_connection.mget = mock.Mock(return_value = fake_points)

    scores = scores_db.ScoresDB(fake_connection)

    # Get the value
    points = scores.get_league_points('ABC')
    # Assert that the right things were called
    fake_connection.keys.assert_called_once_with('match:scores:*:ABC:league')
    fake_connection.mget.assert_called_once_with(*keys)

    # Check that the right result was output
    assert points == 5.0

def test_get_league_points_empty():
    fake_connection = mock.Mock()
    fake_connection.keys = mock.Mock(return_value = [])
    fake_connection.mget = mock.Mock(return_value = [])

    scores = scores_db.ScoresDB(fake_connection)

    # Get the value
    points = scores.get_league_points('ABC')
    # Assert that the right things were called (or not)
    fake_connection.keys.assert_called_once_with('match:scores:*:ABC:league')
    assert not fake_connection.mget.called, "Should not call mget when no matches"

    # Check that the right result was output
    assert points is None

def test_disqualify():
    fake_connection = mock.Mock()
    fake_connection.set = mock.Mock()

    scores = scores_db.ScoresDB(fake_connection)

    scores.disqualify(1, 'ABC')
    # Assert that the right things were called
    fake_connection.set.assert_called_once_with('match:scores:1:ABC:dsq', True)

def test_re_qualify():
    fake_connection = mock.Mock()
    fake_connection.delete = mock.Mock()

    scores = scores_db.ScoresDB(fake_connection)

    scores.re_qualify(1, 'ABC')
    # Assert that the right things were called
    fake_connection.delete.assert_called_once_with('match:scores:1:ABC:dsq')

def test_teams_in_match():
    fake_connection = mock.Mock()
    keys = ['match:scores:1:ABC:game', 'match:scores:1:DEF:game']
    fake_connection.keys = mock.Mock(return_value = keys)

    scores = scores_db.ScoresDB(fake_connection)

    # Get the value
    actual = scores.teams_in_match(1)

    # Assert that the right things were called
    fake_connection.keys.assert_called_once_with('match:scores:1:*:game')

    # Check that the right result was output
    assert actual == ['ABC', 'DEF']

def test_teams_in_match_empty():
    fake_connection = mock.Mock()
    fake_connection.keys = mock.Mock(return_value = [])

    scores = scores_db.ScoresDB(fake_connection)

    # Get the value
    actual = scores.teams_in_match(1)

    # Assert that the right things were called
    fake_connection.keys.assert_called_once_with('match:scores:1:*:game')

    # Check that the right result was output
    assert actual == []

def test_teams_disqualified_in_match():
    fake_connection = mock.Mock()
    keys = ['match:scores:1:ABC:dsq', 'match:scores:1:DEF:dsq']
    fake_connection.keys = mock.Mock(return_value = keys)

    scores = scores_db.ScoresDB(fake_connection)

    # Get the value
    actual = scores.teams_disqualified_in_match(1)

    # Assert that the right things were called
    fake_connection.keys.assert_called_once_with('match:scores:1:*:dsq')

    # Check that the right result was output
    assert actual == ['ABC', 'DEF']

def test_teams_disqualified_in_match_empty():
    fake_connection = mock.Mock()
    fake_connection.keys = mock.Mock(return_value = [])

    scores = scores_db.ScoresDB(fake_connection)

    # Get the value
    actual = scores.teams_disqualified_in_match(1)

    # Assert that the right things were called
    fake_connection.keys.assert_called_once_with('match:scores:1:*:dsq')

    # Check that the right result was output
    assert actual == []

def test_get_match_score():
    fake_connection = mock.Mock()
    fake_connection.get = mock.Mock(return_value = 2)

    scores = scores_db.ScoresDB(fake_connection)

    # Get the value
    actual = scores.get_match_score(1, 'ABC')

    # Assert that the right things were called
    fake_connection.get.assert_called_once_with('match:scores:1:ABC:game')

    # Check that the right result was output
    assert actual == 2

def test_get_match_scores():
    fake_connection = mock.Mock()
    teams = ['ABC', 'DEF']
    fake_get_teams = mock.Mock(return_value = teams)
    fake_connection.mget = mock.Mock(return_value = [2,3])

    scores = scores_db.ScoresDB(fake_connection)
    scores.teams_in_match = fake_get_teams

    # Get the value
    actual = scores.get_match_scores(1)

    # Assert that the right things were called
    fake_get_teams.assert_called_once_with(1)
    fake_connection.mget.assert_called_once_with(*['match:scores:1:ABC:game',
                                                   'match:scores:1:DEF:game'])

    # Check that the right result was output
    assert actual == {'ABC':2, 'DEF':3}

def test_get_match_scores_empty():
    fake_connection = mock.Mock()
    fake_get_teams = mock.Mock(return_value = [])
    fake_connection.mget = mock.Mock(return_value = [2,3])

    scores = scores_db.ScoresDB(fake_connection)
    scores.teams_in_match = fake_get_teams

    # Get the value
    actual = scores.get_match_scores(1)

    # Assert that the right things were called
    fake_get_teams.assert_called_once_with(1)
    assert not fake_connection.mget.called, "Should not query scores we don't have"

    # Check that the right result was output
    assert actual is None

## Commands

def test_perform_set_score():
    fake_set_score = mock.Mock()
    fake_responder = mock.Mock()
    with mock.patch('scores_db.scores.set_match_score', fake_set_score):

        options = { '<match-id>': 1,
                    '<tla>': 'ABC',
                    '<score>': 3 }

        # Run the command
        scores_db.perform_set_score(fake_responder, options)

        # Assert that the right things were called
        fake_set_score.assert_called_once_with(1, 'ABC', 3)

        # Check that the right text was output
        fake_responder.assert_called_once_with('Scored 3 points for ABC in match 1')

def test_perform_get_score():
    fake_get_score = mock.Mock(return_value = 3)
    fake_responder = mock.Mock()
    with mock.patch('scores_db.scores.get_match_score', fake_get_score):

        options = { '<match-id>': 1,
                    '<tla>': 'ABC' }

        # Run the command
        scores_db.perform_get_score(fake_responder, options)

        # Assert that the right things were called
        fake_get_score.assert_called_once_with(1, 'ABC')

        # Check that the right text was output
        fake_responder.assert_called_once_with('Team ABC scored 3 in match 1')

def test_perform_get_score_yaml():
    fake_get_score = mock.Mock(return_value = 3)
    fake_responder = mock.Mock()
    with mock.patch('scores_db.scores.get_match_score', fake_get_score):

        options = { '<match-id>': 1,
                    '<tla>': 'ABC',
                    '--yaml': True }

        # Run the command
        scores_db.perform_get_score(fake_responder, options)

        # Assert that the right things were called
        fake_get_score.assert_called_once_with(1, 'ABC')

        # Check that the right text was output
        fake_responder.assert_called_once_with(yaml.dump({'score':3}))

def test_perform_get_scores():
    results = {'ABC':1, 'DEF':4}
    fake_get_scores = mock.Mock(return_value = results)
    fake_responder = mock.Mock()
    with mock.patch('scores_db.scores.get_match_scores', fake_get_scores):

        options = { '<match-id>': 1,
                    '<tla>': 'ABC' }

        # Run the command
        scores_db.perform_get_scores(fake_responder, options)

        # Assert that the right things were called
        fake_get_scores.assert_called_once_with(1)

        # Check that the right text was output
        fake_responder.assert_has_calls([mock.call('Team ABC scored 1 in match 1'),
                                         mock.call('Team DEF scored 4 in match 1')],
                                        any_order = True)

def test_perform_get_scores_empty():
    fake_get_scores = mock.Mock(return_value = None)
    fake_responder = mock.Mock()
    with mock.patch('scores_db.scores.get_match_scores', fake_get_scores):

        options = { '<match-id>': 1,
                    '<tla>': 'ABC' }

        # Run the command
        scores_db.perform_get_scores(fake_responder, options)

        # Assert that the right things were called
        fake_get_scores.assert_called_once_with(1)

        # Check that the right text was output
        fake_responder.assert_called_once('No scores available for match 1')

def test_perform_get_scores_yaml():
    results = {'ABC':1, 'DEF':4}
    fake_get_scores = mock.Mock(return_value = results)
    fake_responder = mock.Mock()
    with mock.patch('scores_db.scores.get_match_scores', fake_get_scores):

        options = { '<match-id>': 1,
                    '<tla>': 'ABC',
                    '--yaml': True }

        # Run the command
        scores_db.perform_get_scores(fake_responder, options)

        # Assert that the right things were called
        fake_get_scores.assert_called_once_with(1)

        # Check that the right text was output
        fake_responder.assert_called_once_with(yaml.dump({'scores':results}))

def test_perform_get_scores_empty_yaml():
    results = None
    fake_get_scores = mock.Mock(return_value = results)
    fake_responder = mock.Mock()
    with mock.patch('scores_db.scores.get_match_scores', fake_get_scores):

        options = { '<match-id>': 1,
                    '<tla>': 'ABC',
                    '--yaml': True }

        # Run the command
        scores_db.perform_get_scores(fake_responder, options)

        # Assert that the right things were called
        fake_get_scores.assert_called_once_with(1)

        # Check that the right text was output
        fake_responder.assert_called_once_with(yaml.dump({'scores':results}))

def test_calc_league_points():
    match_results = {'ABC':2, 'FED':4, 'GHI':18}
    dsqs = ['GHI']
    fake_get_scores = mock.Mock(return_value = match_results)
    fake_get_dsqs = mock.Mock(return_value = dsqs)
    results = {'ABC':3.0, 'FED': 4.0}
    fake_ranker = mock.Mock(return_value = results)
    fake_set_league_pts = mock.Mock()
    fake_responder = mock.Mock()
    with mock.patch('ranker.get_ranked_points', fake_ranker), \
         mock.patch('scores_db.scores.get_match_scores', fake_get_scores), \
         mock.patch('scores_db.scores.set_league_points', fake_set_league_pts), \
         mock.patch('scores_db.scores.teams_disqualified_in_match', fake_get_dsqs):

        options = { '<match-id>': 1 }

        # Run the command
        scores_db.perform_calc_league_points(fake_responder, options)

        # Assert that the right things were called
        fake_get_scores.assert_called_once_with(1)
        fake_get_dsqs.assert_called_once_with(1)
        fake_ranker.assert_called_once_with(match_results, dsqs)
        fake_set_league_pts.assert_called_once_with(1, results)

        # Check that the right text was output
        fake_responder.assert_has_calls([mock.call('Team ABC earned 3.0 points from match 1'),
                                         mock.call('Team FED earned 4.0 points from match 1')],
                                        any_order = True)

def test_calc_league_points_yaml():
    match_results = {'ABC':2, 'FED':4, 'GHI':18}
    dsqs = ['GHI']
    fake_get_scores = mock.Mock(return_value = match_results)
    fake_get_dsqs = mock.Mock(return_value = dsqs)
    results = {'ABC':3.0, 'FED': 4.0}
    fake_ranker = mock.Mock(return_value = results)
    fake_set_league_pts = mock.Mock()
    fake_responder = mock.Mock()
    with mock.patch('ranker.get_ranked_points', fake_ranker), \
         mock.patch('scores_db.scores.get_match_scores', fake_get_scores), \
         mock.patch('scores_db.scores.set_league_points', fake_set_league_pts), \
         mock.patch('scores_db.scores.teams_disqualified_in_match', fake_get_dsqs):

        options = { '<match-id>': 1,
                    '--yaml': True }

        # Run the command
        scores_db.perform_calc_league_points(fake_responder, options)

        # Assert that the right things were called
        fake_get_scores.assert_called_once_with(1)
        fake_get_dsqs.assert_called_once_with(1)
        fake_ranker.assert_called_once_with(match_results, dsqs)
        fake_set_league_pts.assert_called_once_with(1, results)

        # Check that the right text was output
        fake_responder.assert_called_once_with(yaml.dump({'points':results}))

def test_calc_league_points_empty():
    fake_get_scores = mock.Mock(return_value = None)
    fake_get_dsqs = mock.Mock(return_value = [])
    results = {'ABC':3.0, 'FED': 4.0}
    fake_ranker = mock.Mock(return_value = results)
    fake_set_league_pts = mock.Mock()
    fake_responder = mock.Mock()
    with mock.patch('ranker.get_ranked_points', fake_ranker), \
         mock.patch('scores_db.scores.get_match_scores', fake_get_scores), \
         mock.patch('scores_db.scores.set_league_points', fake_set_league_pts), \
         mock.patch('scores_db.scores.teams_disqualified_in_match', fake_get_dsqs):

        options = { '<match-id>': 1 }

        # Run the command
        scores_db.perform_calc_league_points(fake_responder, options)

        # Assert that the right things were called
        fake_get_scores.assert_called_once_with(1)
        assert not fake_get_dsqs.called
        assert not fake_ranker.called
        assert not fake_set_league_pts.called

        # Check that the right text was output
        fake_responder.assert_called_once_with('No scores available for match 1')

def test_calc_league_points_empty_yaml():
    fake_get_scores = mock.Mock(return_value = None)
    fake_get_dsqs = mock.Mock(return_value = [])
    results = {'ABC':3.0, 'FED': 4.0}
    fake_ranker = mock.Mock(return_value = results)
    fake_set_league_pts = mock.Mock()
    fake_responder = mock.Mock()
    with mock.patch('ranker.get_ranked_points', fake_ranker), \
         mock.patch('scores_db.scores.get_match_scores', fake_get_scores), \
         mock.patch('scores_db.scores.set_league_points', fake_set_league_pts), \
         mock.patch('scores_db.scores.teams_disqualified_in_match', fake_get_dsqs):

        options = { '<match-id>': 1,
                    '--yaml': True }

        # Run the command
        scores_db.perform_calc_league_points(fake_responder, options)

        # Assert that the right things were called
        fake_get_scores.assert_called_once_with(1)
        assert not fake_get_dsqs.called
        assert not fake_ranker.called
        assert not fake_set_league_pts.called

        # Check that the right text was output
        fake_responder.assert_called_once_with(yaml.dump({'points':None}))

def test_get_league_points():
    pts = 7.0
    fake_get_league_pts = mock.Mock(return_value = pts)
    fake_responder = mock.Mock()
    with mock.patch('scores_db.scores.get_league_points', fake_get_league_pts):

        options = { '<tla>': 'ABC' }

        # Run the command
        scores_db.perform_get_league_points(fake_responder, options)

        # Assert that the right things were called
        fake_get_league_pts.assert_called_once_with('ABC')

        # Check that the right text was output
        fake_responder.assert_called_once_with('Team ABC have 7.0 league points')

def test_get_league_points_yaml():
    pts = 7.0
    fake_get_league_pts = mock.Mock(return_value = pts)
    fake_responder = mock.Mock()
    with mock.patch('scores_db.scores.get_league_points', fake_get_league_pts):

        options = { '<tla>': 'ABC',
                    '--yaml': True }

        # Run the command
        scores_db.perform_get_league_points(fake_responder, options)

        # Assert that the right things were called
        fake_get_league_pts.assert_called_once_with('ABC')

        # Check that the right text was output
        fake_responder.assert_called_once_with(yaml.dump({'points':pts}))

def test_get_league_points_empty():
    pts = None
    fake_get_league_pts = mock.Mock(return_value = pts)
    fake_responder = mock.Mock()
    with mock.patch('scores_db.scores.get_league_points', fake_get_league_pts):

        options = { '<tla>': 'ABC' }

        # Run the command
        scores_db.perform_get_league_points(fake_responder, options)

        # Assert that the right things were called
        fake_get_league_pts.assert_called_once_with('ABC')

        # Check that the right text was output
        fake_responder.assert_called_once_with('No scores available for team ABC')

def test_get_league_points_empty_yaml():
    pts = None
    fake_get_league_pts = mock.Mock(return_value = pts)
    fake_responder = mock.Mock()
    with mock.patch('scores_db.scores.get_league_points', fake_get_league_pts):

        options = { '<tla>': 'ABC',
                    '--yaml': True }

        # Run the command
        scores_db.perform_get_league_points(fake_responder, options)

        # Assert that the right things were called
        fake_get_league_pts.assert_called_once_with('ABC')

        # Check that the right text was output
        fake_responder.assert_called_once_with(yaml.dump({'points':pts}))

def test_get_dsqs():
    dsqs = ['ABC', 'DEF']
    fake_get_dsqs = mock.Mock(return_value = dsqs)
    fake_responder = mock.Mock()
    with mock.patch('scores_db.scores.teams_disqualified_in_match', fake_get_dsqs):

        options = { '<match-id>': 1 }

        # Run the command
        scores_db.perform_get_dsqs(fake_responder, options)

        # Assert that the right things were called
        fake_get_dsqs.assert_called_once_with(1)

        # Check that the right text was output
        fake_responder.assert_called_once_with('Team(s) ABC, DEF were disqualified from match 1')

def test_get_dsqs_yaml():
    dsqs = ['ABC', 'DEF']
    fake_get_dsqs = mock.Mock(return_value = dsqs)
    fake_responder = mock.Mock()
    with mock.patch('scores_db.scores.teams_disqualified_in_match', fake_get_dsqs):

        options = { '<match-id>': 1,
                    '--yaml': True }

        # Run the command
        scores_db.perform_get_dsqs(fake_responder, options)

        # Assert that the right things were called
        fake_get_dsqs.assert_called_once_with(1)

        # Check that the right text was output
        fake_responder.assert_called_once_with(yaml.dump({'dsqs': dsqs}))

def test_get_dsqs_empty():
    fake_get_dsqs = mock.Mock(return_value = [])
    fake_responder = mock.Mock()
    with mock.patch('scores_db.scores.teams_disqualified_in_match', fake_get_dsqs):

        options = { '<match-id>': 1 }

        # Run the command
        scores_db.perform_get_dsqs(fake_responder, options)

        # Assert that the right things were called
        fake_get_dsqs.assert_called_once_with(1)

        # Check that the right text was output
        fake_responder.assert_called_once_with('No teams were disqualified from match 1')

def test_get_dsqs_empty_yaml():
    dsqs = []
    fake_get_dsqs = mock.Mock(return_value = dsqs)
    fake_responder = mock.Mock()
    with mock.patch('scores_db.scores.teams_disqualified_in_match', fake_get_dsqs):

        options = { '<match-id>': 1,
                    '--yaml': True }

        # Run the command
        scores_db.perform_get_dsqs(fake_responder, options)

        # Assert that the right things were called
        fake_get_dsqs.assert_called_once_with(1)

        # Check that the right text was output
        fake_responder.assert_called_once_with(yaml.dump({'dsqs': dsqs}))

def test_disqualify():
    fake_disqualify = mock.Mock()
    fake_responder = mock.Mock()
    with mock.patch('scores_db.scores.disqualify', fake_disqualify):

        options = { '<match-id>': 1,
                    '<tla>': 'ABC' }

        # Run the command
        scores_db.perform_disqualify(fake_responder, options)

        # Assert that the right things were called
        fake_disqualify.assert_called_once_with(1, 'ABC')

        # Check that the right text was output
        fake_responder.assert_called_once_with('Disqualified ABC in match 1')

def test_re_qualify():
    fake_re_qualify = mock.Mock()
    fake_responder = mock.Mock()
    with mock.patch('scores_db.scores.re_qualify', fake_re_qualify):

        options = { '<match-id>': 1,
                    '<tla>': 'ABC' }

        # Run the command
        scores_db.perform_re_qualify(fake_responder, options)

        # Assert that the right things were called
        fake_re_qualify.assert_called_once_with(1, 'ABC')

        # Check that the right text was output
        fake_responder.assert_called_once_with('Re-qualified ABC in match 1')
