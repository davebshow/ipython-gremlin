"""Simple interface for keeping track of DB connections and aliases"""
import asyncio
from urllib.parse import urlparse

from aiogremlin.driver import connection


class RegistryConnection:
    """Wrapper for :py:class:`aiogremlin.driver.connection.Connection`"""
    def __init__(self, conn, alias):
        self._conn = conn
        self._alias = alias

    def __repr__(self):
        return 'Connection at {} aliased as {}'.format(self.uri, self._alias)

    @property
    def uri(self):
        return self._conn._url

    @property
    def alias(self):
        return self._alias

    @alias.setter
    def alias(self, alias):
        self._alias = alias

    @property
    def loop(self):
        return self._conn._loop

    async def write(self, message):
        """Write message to Gremlin Server"""
        return await self._conn.write(message)

    async def close(self):
        """Close underlying connections"""
        return await self._conn.close()


class ConnectionRegistry:
    """Issue and keep track of database connections."""

    current = None
    connections = {}
    _loop = asyncio.get_event_loop()

    @classmethod
    def get(cls, descriptors, config=None):
        """Get a connection from the registry based on the descriptor"""
        primary, secondary = descriptors
        if primary:
            cls.current = cls.connections.get(primary)
            if not cls.current:
                cls.currernt = cls._get_connection(primary, secondary, config)
        elif not cls.current:
            cls.current = cls._get_connection(config.uri, None, config)
        return cls.current

    @classmethod
    def close(cls):
        """Close all DB connections"""
        conns = set(cls.connections.values())

        async def go(conns):
            for conn in conns:
                await conn.close()

        cls._loop.run_until_complete(go(conns))

    @classmethod
    def set_connection_alias(cls, descriptors, config):
        primary, secondary = descriptors
        if not secondary:
            raise RuntimeError('Improperly formatted alias descriptors')
        conn = cls.connections.get(primary)
        if not conn:
            conn = cls._get_connection(primary, secondary, config)
        else:
            if conn.alias != secondary:
                cls.connections.pop(conn.alias)
                cls.connections[secondary] = conn

    @classmethod
    def set_current_connection(cls, descriptors, config):
        primary, secondary = descriptors
        if not primary:
            raise RuntimeError('Please specify connection to set')
        conn = cls.connections.get(primary)
        if not conn:
            conn = cls._get_connection(primary, secondary, config)
        cls.current = conn

    @classmethod
    def _get_connection(cls, primary, secondary, config):
        try:
            conn = cls._loop.run_until_complete(
                connection.Connection.open(
                    primary, cls._loop, username=config.username,
                    password=config.password,
                    response_timeout=config.response_timeout))
        except:
            raise Exception(
                'Unable to establish connection at URI: {}'.format(primary))
        else:
            if not secondary:
                secondary = cls._create_secondary(primary)
            conn = RegistryConnection(conn, secondary)
            cls.connections[primary] = conn
            cls.connections[secondary] = conn
            return conn

    @classmethod
    def _create_secondary(cls, primary):
        alias = urlparse(primary).netloc.split(':')[0]
        print('Alias-- {} --created for database at {}'.format(
            alias, primary))
        return alias
