
from collections import namedtuple
from datetime import datetime

from match_db import MatchDB
import redis_client
from team_db import TeamDB
from utils import parse_time

# An object representing a match
Match = namedtuple("Match", ["name", "time"])

# An object representing a team
Team = namedtuple("Team", ["id", "college", "name"])

class PoltergeistReader(object):
    "Object for reading all the match info from poltergeist"

    def __init__(self):
        self.redis = redis_client.connection
        self.team_db = TeamDB(self.redis)
        self.match_db = MatchDB(self.redis)

    @property
    def teams(self):
        "Dictionary of teams in the competition"
        tlas = self.team_db.list()
        teams = {}

        for tla in tlas:
            info = self.team_db.get(tla)
            teams[tla] = Team(tla, info["college"], info["name"])

        return teams

    @property
    def matches(self):
        "Matches in the match schedule"
        match_ids = self.match_db.matches_between(0,0xffffffffffffffff)
        matches = []

        for match_id, timestamp in match_ids:
            match = Match( match_id,
                           datetime.fromtimestamp( timestamp ) )

            matches.append(match)

        return matches

    @property
    def match_scores(self):
        "The match scores"
        pass

    @property
    def league_scores(self):
        "The league scores"
        pass
