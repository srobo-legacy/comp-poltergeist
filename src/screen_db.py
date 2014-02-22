"""Screen database."""

import redis_client
import control
import re

class ScreenDB(object):
    """A screen database."""

    def __init__(self, redis_connection):
        """Creates a new database wrapper around the given connection."""
        self._conn = redis_connection

    def set_mode(self, screen, mode):
        self._conn.set('screen:{0}:mode'.format(screen),
                                    mode)
        self._conn.publish('screen:update', 'update')

    def set_override(self, screen, override):
        if override is not None:
            self._conn.set('screen:{0}:override'.format(screen),
                                        override)
        else:
            self._conn.delete('screen:{0}:override'.format(screen))
        self._conn.publish('screen:update', 'update')

    def list(self):
        screens = self._conn.keys('screen:*:mode')
        entries = {}
        for screen in screens:
            screenID = screen.split(':')[1]
            mode = self._conn.get('screen:{0}:mode'.format(screenID))
            host = self._conn.get('screen:{0}:host'.format(screenID))
            entries[screenID] = {'mode': mode,
                                 'host': host}
        return entries

screens = ScreenDB(redis_client.connection)

@control.handler('screen-list')
def perform_screen_list(responder, options):
    screen_list = screens.list()
    for screen, settings in screen_list.iteritems():
        if settings['host'] is None:
            online_string = 'offline'
        else:
            online_string = 'online from {0} port {1}'.format(*settings['host'].split(' '))
        responder('{0} - {1} ({2})'.format(screen,
                                           settings['mode'],
                                           online_string))

@control.handler('screen-set-mode')
def perform_screen_set_mode(responder, options):
    screens.set_mode(options['<id>'], options['<mode>'])
    responder('Mode set.')

@control.handler('screen-override')
def perform_screen_override(responder, options):
    screens.set_override(options['<id>'], options['<message>'])
    responder('Override set.')

@control.handler('screen-clear-override')
def perform_screen_clear_override(responder, options):
    screens.set_override(options['<id>'], None)
    responder('Override cleared.')

def got_screen(name):
    control.broadcast('Screen connected: {0}'.format(name))

redis_client.add_subscribe('screen:connect', got_screen)
