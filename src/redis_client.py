
import redis

import config
config.load_config('config.yaml')

connection = None

def run_redis_client(on_started = None):
    global connection
    connection = redis.Redis(config.redis['host'],
                             config.redis['port'],
                             config.redis['db'])
    if on_started:
        on_started()

def add_subscribe(key, callback):
    """
    Base implementation can't subscribe to anything as it only has a
    short-lived connection. Long-running frontends should replace this
    function with one that actually subscribes.
    """
    pass
