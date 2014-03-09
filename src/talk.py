
import yaml
import control

# Import the relevant command modules.
# These self-subscribe to the control hanlder, but need to get imported
import schedule_commands
import team_commands
import scores_commands
import match_commands

def command(cmd):
    responses = []
    control.handle(cmd, responses.append)
    return "\n".join(responses)

def command_yaml(cmd):
    cmd += ' --yaml'
    raw_data = command(cmd)
    data = yaml.load(raw_data)
    return data
