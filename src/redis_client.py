
import redis

from config import config

connection = None

def run_redis_client(on_started = None):
    global connection
    host = config.get('redis', 'host')
    port = int(config.get('redis', 'port'))
    db = int(config.get('redis', 'db'))

    # NOTE: Some of the argument orderings are different between Redis
    # and StrictRedis. Think carefully before changing this.
    connection = redis.StrictRedis(host, port, db)

    if on_started:
        on_started()

def add_subscribe(key, callback):
    """
    Base implementation can't subscribe to anything as it only has a
    short-lived connection. Long-running frontends should replace this
    function with one that actually subscribes.
    """
    pass

if connection is None:
    run_redis_client()
