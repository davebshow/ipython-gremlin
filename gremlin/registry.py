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
            elif secondary:
                cls._replace_alias(cls.current, secondary)
        elif not cls.current:
            cls.current = cls._get_connection(config.uri, None, config)
        return cls.current

    @classmethod
    def close(cls, connection_str=None):
        """Close DB connections"""
        if connection_str:
            conn = cls.connections.pop(connection_str)
            if not conn:
                raise RuntimeError('Specified conn does not exist')
            if connection_str == conn.uri:
                cls.connections.pop(conn.alias)
            else:
                cls.connections.pop(conn.uri)
            if conn is cls.current:
                cls.current = None
            conns = [conn]
        else:
            keys= set(cls.connections.keys())
            conns = set()
            for k in keys:
                conn = cls.connections.pop(k)
                conns.add(conn)
            cls.current = None

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
            cls._replace_alias(conn, secondary)


    @classmethod
    def _replace_alias(cls, conn, alias):
        if conn.alias != alias:
            cls.connections.pop(conn.alias)
            cls.connections[alias] = conn
            conn.alias = alias
            print('Alias-- {} --created for database at {}'.format(
                alias, conn.uri))

    @classmethod
    def set_current_connection(cls, descriptors, config):
        primary, secondary = descriptors
        if not primary:
            raise RuntimeError('Please specify connection to set')
        conn = cls.connections.get(primary)
        if not conn:
            conn = cls._get_connection(primary, secondary, config)
        cls.current = conn
        print('Now using connection at {}'.format(conn.uri))

    @classmethod
    def _get_connection(cls, primary, secondary, config):
        try:
            conn = cls._loop.run_until_complete(
                connection.Connection.open(
                    primary, cls._loop, username=config.username,
                    password=config.password,
                    response_timeout=config.response_timeout,
                    ssl_context=config.ssl_context))
        except:
            raise Exception(
                'Unable to establish connection at URI: {}'.format(primary))
        else:
            if not secondary:
                secondary = cls._create_secondary(primary)
            conn = RegistryConnection(conn, secondary)
            cls.connections[primary] = conn
            cls.connections[secondary] = conn
            print('Alias-- {} --created for database at {}'.format(
                secondary, primary))
            return conn

    @classmethod
    def _create_secondary(cls, primary):
        alias = urlparse(primary).netloc.split(':')[0]
        return alias
