"""compd-cli

Usage:
  cli.py [options] <command-detail>...

Options:
  -h --help                 Display this help.
  --yaml                    Call the command with a --yaml option
"""

from docopt import docopt

import talk

options = docopt(__doc__)

cmd_details = options['<command-detail>']
if options['--yaml']:
    cmd_details.append('--yaml')
cmd = ' ' .join(cmd_details) + "\n"

#print cmd
back = talk.command(cmd)
print back
