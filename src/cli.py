"""compd-cli

Usage:
  cli.py [options] <command-detail>...

Options:
  -h --help                 Display this help.
  --yaml                    Call the command with a --yaml option
  -c <file> --config <file> Use an alternative config.yaml.
"""

from docopt import docopt
import os.path
import socket
import sys

import talk
import config

options = docopt(__doc__)

config.load_config(options['--config'])

cmd_details = options['<command-detail>']
if options['--yaml']:
    cmd_details.append('--yaml')
cmd = ' ' .join(cmd_details) + "\n"

#print cmd
back = talk.command(cmd)
print back
