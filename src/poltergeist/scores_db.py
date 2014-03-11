"""Team scores database."""

import re

class ScoresDB(object):
    """A scores database."""

    def __init__(self, redis_connection):
        """Creates a new database wrapper around the given connection."""
        self._conn = redis_connection

    def set_match_score(self, match, tla, match_score):
        """Sets the score for a given team in a given match."""
        self._conn.set('match:scores:{0}:{1}:game'.format(match, tla),
                                    match_score)

    def set_league_points(self, match, points):
        """Sets the league points for all the teams in a given match."""

        keys = ['match:scores:{0}:{1}:league'.format(match, tla) for tla in points.keys()]
        keyed_points = dict(zip(keys, points.values()))

        self._conn.mset(keyed_points)

    def get_league_points(self, tla):
        """Gets the league points a given team."""

        keys = self._conn.keys('match:scores:*:{0}:league'.format(tla))
        if len(keys) == 0:
            return None
        points = self._conn.mget(*keys)
        return sum(points)

    def disqualify(self, match, tla):
        """Disqualifies a given team in a given match."""
        self._conn.set('match:scores:{0}:{1}:dsq'.format(match, tla), True)

    def re_qualify(self, match, tla):
        """Re-qualifies a given team in a given match.
        Just in case a judge changes their mind."""
        self._conn.delete('match:scores:{0}:{1}:dsq'.format(match, tla))

    def teams_in_match(self, match):
        # Get a list of the teams in a given match for which we have game scores
        keys = self._conn.keys('match:scores:{0}:*:game'.format(match))
        teams = [re.match('match:scores:{0}:([a-zA-Z0-9]*):game'.format(match), key).group(1)
                             for key in keys]
        return teams

    def teams_disqualified_in_match(self, match):
        # Get a list of the teams disqualified in a given match
        keys = self._conn.keys('match:scores:{0}:*:dsq'.format(match))
        teams = [re.match('match:scores:{0}:([a-zA-Z0-9]*):dsq'.format(match), key).group(1)
                             for key in keys]
        return teams

    def get_match_scores(self, match):
        # Get a dictionary of team => game points for a given match
        teams = self.teams_in_match(match)
        if len(teams) == 0:
            return None

        raw_scores = \
            self._conn.mget(*['match:scores:{0}:{1}:game'.format(match, tla)
                                                   for tla in teams])

        match_scores = dict(zip(teams, raw_scores))
        return match_scores

    def get_match_score(self, match, tla):
        """Gets the score for a given team in a given match.

        Returns something"""
        value = self._conn.get('match:scores:{0}:{1}:game'.format(match, tla))
        return value
