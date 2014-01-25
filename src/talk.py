
import yaml
import control

def command(cmd):
    responses = []
    control.handle(cmd, responses.append)
    return "\n".join(responses)

def command_yaml(cmd):
    cmd += ' --yaml'
    raw_data = command(cmd)
    data = yaml.load(raw_data)
    return data
