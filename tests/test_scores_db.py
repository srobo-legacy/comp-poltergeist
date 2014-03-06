
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
