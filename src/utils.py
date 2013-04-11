
import parsedatetime
import time
import datetime

class ParseError(Exception):
    """Indicates an error when parsing time values."""
    pass

def parse_time(s):
    """Parse a human-readable time format into a UNIX timestamp."""
    calendar = parsedatetime.Calendar()
    result, accuracy = calendar.parse(s)
    if accuracy == 0:
        raise ParseError()
    return time.mktime(result)

def format_time(n):
    """Convert from a UNIX timestamp into a human-readable time format."""
    return str(datetime.datetime.fromtimestamp(n))

