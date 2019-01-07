"""Default configuration for GremlinMagic"""
import collections


DEFAULT_CONFIG = {
    'aliases': {'g': 'g'},
    'password': '',
    'response_timeout': None,
    'ssl_context': None,
    'uri': 'ws://localhost:8182/gremlin',
    'username': '',
    'use_local_namespace': True,
    'warnings': False
}


DefaultConfig = collections.namedtuple(
    'DefaultConfig', list(DEFAULT_CONFIG.keys()))


defaults = DefaultConfig(**DEFAULT_CONFIG)
