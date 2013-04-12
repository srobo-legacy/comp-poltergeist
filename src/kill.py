import control
import redis_client

last_kill = None

def got_kill(source):
    global last_kill
    if source:
        if source != last_kill:
            control.broadcast('Kill received: {0}'.format(source))
            last_kill = source
    else:
        last_kill = None
        control.broadcast('Kill cleared.')

@control.handler('kill')
def kill(responder, options):
    redis_client.connection.publish('comp:kill', 'console')

@control.handler('unkill')
def unkill(responder, options):
    redis_client.connection.publish('comp:kill', '')

redis_client.add_subscribe('comp:kill', got_kill)

