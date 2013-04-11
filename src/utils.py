
import dateutil.parser
import time
import datetime

def parse_time(s):
    """Parse a human-readable time format into a UNIX timestamp."""
    then_dt = dateutil.parser.parse(s)
    stamp = time.mktime(then_dt.timetuple())
    return stamp

def format_time(n):
    """Convert from a UNIX timestamp into a human-readable time format."""
    return str(datetime.datetime.fromtimestamp(n))

