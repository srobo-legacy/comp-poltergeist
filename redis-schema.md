
Information about the shape of the data in redis.


# Matches

Keys related to competition matches.

## `match:matches:<match-id>:format`
The type of match, either "league" or "knockout".

## `match:matches:<match-id>:teams`
A list of team identifiers which are in the match.

## `match:schedule`
A sorted set of `match-id`s.
The keys of the sorted set are unix timestamps for the match


# Schedule

Information about various (non-match) events which occur during the competition.

## `comp:events:<event-id>`
The type of the event. One of: "league", "knockout", "lunch", "open",
 "tinker", "photo", "prizes" or "briefing".

## `comp:schedule`
A sorted set of `event-id`s.
The keys of the sorted set are unix timestamps for the event.


# Scores

## `match:scores:<match-id>:<team-id>:game`
The game score achieved by the given team in the given match.
This is expected to be a number, and its meaning will depend on the game
being played at the competition.

## `match:scores:<match-id>:<team-id>:league`
The league points earned by the given team from the given match.
This is a floating point number, as teams may score fractional league points
in the case of game ties.

## `match:scores:<match-id>:<team-id>:dsq`
A value indicating whether or not the given team was disqualified from
the given match.
Only valid if the value is `True`, and should not be present if the value
would be `False`.


# Screen

Information to be shown on the competition screens.
_**Note:** This portion of the database has not been used._

## `screen:<screen-id>:mode`
The mode that the given screen is in.

## `screen:<screen-id>:override`
Some override value for the given screen id.
Should only be present if the override is required.

## `screen:<screen-id>:host`
Information about the host on which the screen is running.
Probably.


# Teams

Information about the teams at the competition.

## `team:<team-id>:college`
The name of college (or similar organisation) the given team is from.

## `team:<team-id>:name`
The name of the given team.

## `team:<team-id>:notes`
Some notes about the given team.

## `team:<team-id>:present`
A boolean value indicating whether or not the team has turned up to the
competition.
