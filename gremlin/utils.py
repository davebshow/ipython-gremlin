"""Utility functions to support GremlinMagic operations"""
import json
import re

from aiogremlin.gremlin_python.driver import request
from aiogremlin.remote.driver_remote_side_effects import (
    RemoteTraversalSideEffects)
from gremlin import registry, resultset


def parse(connection_str):
    """Parse connection string passed by user"""
    if ' as ' in connection_str.lower():
        descriptors = re.split(' as ', connection_str,  flags=re.IGNORECASE)
    else:
        descriptors = (connection_str, None)
    return descriptors


def _sanitize_namespace(user_ns):
    bindings = {}
    for k, v in user_ns.items():
        try:
            json.dumps(v)
        except:
            pass
        else:
            bindings[k] = v
    return bindings


def submit(gremlin, user_ns, aliases, conn):
    """
    Submit a script to the Gremlin Server using the IPython namespace
    using the IPython namespace to pass bindings using Magics configuration
    and a connection registered with
    :py:class:`ConnectionRegistry<gremlin.registry.ConnectionRegistry>`
    """
    loop = conn.loop
    bindings = _sanitize_namespace(user_ns)
    message = request.RequestMessage(
        processor='', op='eval',
        args={'gremlin': gremlin, 'aliases': aliases, 'bindings': bindings})
    return loop.run_until_complete(_submit(conn, message))


async def _submit(conn, message):
    result_set = await conn.write(message)
    results = await result_set.all()
    return resultset.ResultSet(results, message)
