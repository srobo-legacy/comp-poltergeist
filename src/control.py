"""compctl

Usage:
  compctl usage
  compctl version
  compctl schedule (lunch | league | knockout | open | briefing | photo | prizes | tinker) <time>
  compctl unschedule <id>
  compctl show-schedule <from> <to>
  compctl add-team <tla> <name> <college>
  compctl del-team <tla>
  compctl set-team-name <tla> <name>
  compctl set-team-college <tla> <college>
  compctl set-team-notes <tla> <notes>
  compctl append-note <tla> <note>
  compctl set-team-present <tla>
  compctl set-team-absent <tla>
  compctl list-teams [--yaml]
  compctl team [--yaml] <tla>
  compctl set-score <match-id> <tla> <score>
  compctl get-score [--yaml] <match-id> <tla>
  compctl get-scores [--yaml] <match-id>
  compctl calc-league-points [--yaml] <match-id>
  compctl get-league-points [--yaml] <tla>
  compctl get-dsqs [--yaml] <match-id>
  compctl disqualify <match-id> <tla>
  compctl re-qualify <match-id> <tla>
  compctl add-match [--knockout] <name> <time>
  compctl del-match <name>
  compctl set-match-teams <name> <team>...
  compctl get-match-teams [--yaml] <match-id>
  compctl get-delay [<when>]
  compctl set-delay <delay> [<when>]
  compctl clear-match-teams <name>
  compctl list-matches [--yaml] <from> <to>
  compctl kill
  compctl unkill

"""

import shlex
from subprocess import check_output, CalledProcessError
import re

from docopt import docopt, DocoptExit

class CommandError(Exception):
    def __init__(self, message = None):
        Exception.__init__(self, message)

class CommandMissingError(CommandError):
    def __init__(self):
        message = "The requested command has not been registered"
        CommandError.__init__(self, message)

class CommandParseError(CommandError):
    pass

def parse(cmd):
    parts = shlex.split(cmd.strip())
    try:
        options = docopt(__doc__, argv = parts,
                         help = False, version = None)
        return options
    except DocoptExit:
        raise CommandParseError()

HANDLERS = {}

def handler(subcommand):
    def wrapper(fn):
        HANDLERS[subcommand] = fn
        return fn
    return wrapper

def dispatch(options, responder):
    for name, callback in HANDLERS.iteritems():
        if options.get(name):
            callback(responder, options)
            return
    raise CommandMissingError()

@handler('usage')
def handle_usage(responder, opts):
    regex = re.compile('  compctl (.*)')
    for line in __doc__.split('\n')[3:]:
        match = regex.match(line)
        if match:
            responder('Usage: {0}'.format(match.group(1)))

GIT_VERSION = None

@handler('version')
def get_version(responder, opts):
    global GIT_VERSION
    if not GIT_VERSION:
        try:
            GIT_VERSION = check_output(('git', 'describe', '--always')).strip()
        except CalledProcessError:
            GIT_VERSION = '?'
    responder(GIT_VERSION)

def default_responder(output):
    print output

def handle(cmd, responder = default_responder, no_auto_fail = False,
           short_fail = True):
    try:
        dispatch(parse(cmd), responder)
    except CommandError as ce:
        if no_auto_fail:
            raise
        elif short_fail:
            if isinstance(ce, CommandParseError):
                responder("Command '{0}' not recognised. Check 'usage' for accepted commands.".format(cmd))
            elif isinstance(ce, CommandMissingError):
                responder("No handler for '{0}' has been registered!".format(cmd))
            else:
              responder('Syntax error.')
        else:
            handle('usage', responder, no_auto_fail = True)

RECEIVERS = {}

def broadcast(message):
    for receiver in RECEIVERS.itervalues():
        receiver(message)

def subscribe(handler):
    key = object()
    RECEIVERS[key] = handler
    def unsubscribe():
        del RECEIVERS[key]
    return unsubscribe

