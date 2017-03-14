"""Default configuration for GremlinMagic"""
import collections


DEFAULT_CONFIG = {
    'aliases': {'g': 'g'},
    'password': '',
    'response_timeout': None,
    'side_effects': False,
    'uri': 'ws://localhost:8182/gremlin',
    'username': ''
}


DefaultConfig = collections.namedtuple(
    'DefaultConfig', list(DEFAULT_CONFIG.keys()))


defaults = DefaultConfig(**DEFAULT_CONFIG)
